# SSHの公開鍵による認証を試す

## SSHサーバー用イメージの準備・起動
```sh
docker pull testcontainers/sshd:1.3.0
docker run -d --name server testcontainers/sshd:1.3.0
```

## SSHクライアント用イメージの準備
Alpineをベースにしてopenssh-clientをインストールしたイメージを作成。

```sh
# Dockerfile作成
cat <<EOF>Dockerfile
FROM alpine:latest

RUN apk add --no-cache openssh-client
EOF

# イメージのビルド
docker build -t ssh-client .
```

## SSHサーバーのIP確認
`172.17.0.2`
```sh
$ docker exec -it server ifconfig

eth0      Link encap:Ethernet  HWaddr 02:42:AC:11:00:02  
          inet addr:172.17.0.2  Bcast:172.17.255.255  Mask:255.255.0.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1735 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1628 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:189746 (185.2 KiB)  TX bytes:184638 (180.3 KiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

## SSH接続 - パスワード認証
まずは普通にパスワード認証で接続してみる。

```sh
# SSHクライアントを起動してシェルを取得
$ docker run --rm --name client -it ssh-client ash
```

```sh
# SSHサーバーへ接続
# Are you sure you want to continue connecting (yes/no/[fingerprint])?はyes
# rootのパスワードはroot
$ ssh root@172.17.0.2

The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:FZig6IVRte6eR9g34cdexVGYaK8qrJbvPEJ4S/HNCtA.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
root@172.17.0.2's password: 
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <https://wiki.alpinelinux.org/>.

You can setup the system with the command: setup-alpine

You may change this message by editing /etc/motd.

3b6bc5001a55:~# 
```

### MEMO - rootのパスワード確認
https://hub.docker.com/layers/testcontainers/sshd/1.3.0/images/sha256-7dc5a534990619c4c785003dc19352ad651a40fb910ea69d24c24b1a93c3e6bc


## SSHクライアントで秘密鍵、公開鍵の作成
次に公開鍵による接続のため、秘密鍵、公開鍵を作成する。
パスフレーズは入力しない。

ホームディレクトリ配下の.sshディレクトリに秘密鍵`id_ed25519`、公開鍵は`id_ed25519.pub`で作成される。  
ed25519はデフォルトの暗号化方式名。オプションでrsaなども指定できる。

```sh
$ ssh-keygen

Generating public/private ed25519 key pair.
Enter file in which to save the key (/root/.ssh/id_ed25519): 
Enter passphrase for "/root/.ssh/id_ed25519" (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/.ssh/id_ed25519
Your public key has been saved in /root/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:xOgvB1YSXw4tBSsqEHjEuTHQThe4O+Zd9hXNtIQ4x68 root@8c430b883d4c
The key's randomart image is:
+--[ED25519 256]--+
|+=.o... o*o.     |
|..X .  =+== o    |
|.+ *  + *+.* .   |
| .+  o =  . =    |
|  ... + S  o     |
|  +. .oo  E      |
| o o o..o.       |
|  . .  o.        |
|                 |
+----[SHA256]-----+
```

## SSHクライアントで作成した公開鍵をSSHサーバーへ登録
```sh
# 鍵の名前やパスはデフォルトで作成したので指定しなくて良い。
$ ssh-copy-id root@172.17.0.2

/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
expr: warning: '^ERROR: ': using '^' as the first character
of a basic regular expression is not portable; it is ignored
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@172.17.0.2's password: 

Number of key(s) added: 1

Now try logging into the machine, with: "ssh 'root@172.17.0.2'"
and check to make sure that only the key(s) you wanted were added.
```

## 公開鍵で接続
SSHクライアントからSSH接続するとパスワードを求められずに接続できる。
```sh
ssh root@172.17.0.2

Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <https://wiki.alpinelinux.org/>.

You can setup the system with the command: setup-alpine

You may change this message by editing /etc/motd.

622fd82e0aca:~# 
```
### MEMO
SSHサーバーに登録した公開鍵はホームディレクトリ配下の.ssh/authorized_keysに登録される。
```sh
cat .ssh/authorized_keys 
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHUex5dAF1irFy2VWvLcbjXhAgdL13NaIkpFrZu6Kx4f root@9e1dcdb08e8b
```

## 後片付け
```sh
docker rm -f server
```