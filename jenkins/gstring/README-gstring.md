# Groovyで定義した変数をshellで参照する
Jenkinsfileを記述しているときにGroovyで記述した変数をShell側で参照できずにハマったのでメモ。

## Jenkins構築
検証に利用するJenkinsの構築。
といってもdocker runして起動し、ナビ通り進めるだけ。

### 公式イメージ
- https://hub.docker.com/_/jenkins

### Jenkins起動
```sh
# イメージのpull
docker pull jenkins/jenkins:slim

# Jenkins起動
docker run -p 8080:8080 -p 50000:50000 -v $(pwd)/var/jenkins_home:/var/jenkins_home jenkins/jenkins:slim
```

## 本題
以下のように記述し、groovy側で定義した変数をshell側で参照しようとしたところ参照できない。

```groovy
def NAME = "world"
sh 'echo Hello! $NAME'
```
```log
Hello! 
```

### 原因
Shell側でNAMEという変数は定義されていないため出力するとブランクとなる。

以下が認識できていなかった。
- GroovyとShell側では変数を共有していないということ。
- シングルクォートで囲むとリテラルとして扱われるということ。

### 解決策
Gstringを使う。
GStringとはダブルクォートで囲まれた文字列のこと。
1行の場合は1つ、複数行記述する場合は3つのダブルクォートで囲む。

これにより、変数がGroovy側で先に展開され、
Shell側で`echo Hello! world`が実行される。

```groovy
def NAME = "world"
sh "echo Hello! $NAME"

// 複数行で記述する場合
sh """
    echo Hello! $NAME
    echo Hello! $NAME
"""
```
```log
Hello! world
```
ちなみに、シングルクォートでも3つにすることで複数行のリテラルとして記述できる。

### 解決策2
環境変数として設定するとShell側でも参照できる。
```groovy
env.NAME = "world"
sh 'echo Hello! $NAME'
```
