# GitHub Actions
基本的な[GitHub Docs](https://docs.github.com/ja/actions/about-github-actions)

## やりたいこと
- ブログの記事をGitHubで管理したい。
- リポジトリにPushしたら自動でBloggerに投稿。
- 画像もGitHubのリポジトリを参照する。

## Google OAuth2.0認証 設定手順
[Blogger API Docs](https://developers.google.com/blogger?hl=ja)

### Google Cloud
プロジェクトは作成済みであることを前提とする。

### Blogger APIの有効化
作成したGoogle Cloudプロジェクトで、Blogger APIを有効にします。
Google Cloud ConsoleのAPIライブラリで「Blogger API」を検索し、有効にしてください。
Blogger APIの公式ドキュメントに沿って作成することも可能です。

### Service Accountの作成
GitHub ActionsからBlogger APIにアクセスするために、サービスアカウントを作成します。
Google Cloud ConsoleのIAMと管理 > サービスアカウントで、新しいサービスアカウントを作成します

### キーの作成

サービスアカウントの認証に使用するJSON形式のキーファイルを作成します。
Google Cloud Consoleのサービスアカウントの詳細ページで、[鍵]タブを選択し、
[キーを追加] > [新しい鍵を作成]を選択。キーのタイプは[JSON]を選択。

### GitHubリポジトリへのシークレット登録
作成したサービスアカウントキーの内容を、GitHubリポジトリのシークレットとして登録。リポジトリの設定 > Secrets and variables > Actionsで、「New repository secret」をクリックし、キーの名前（例: GOOGLE_CREDENTIALS）と値（JSONキーファイルの内容）を入力して保存。

## GitHub Actions から Google Cloud に認証する
https://github.com/google-github-actions/auth

## md -> html変換
https://pandoc-doc-ja.readthedocs.io/ja/latest/users-guide.html

## Troubleshooting
発生した諸々のエラーと対処。

### git diff 実行時にエラー
GitHub Actionsのジョブにて以下のように`git diff`したところエラーとなった。
```sh
git diff --name-only ${{ github.event.before }}..HEAD)
```
```log
fatal: Invalid revision range ef1dd6de85606d4627addee932fd51ba7bff9e7d..HEAD
Error: Process completed with exit code 128.
```
#### 原因
actions/checkoutの`fetch-depth`のデフォルトは`1`で、
その場合、最新の履歴のみフェッチされ一つ前の履歴はfetchされていないから。

https://github.com/actions/checkout?tab=readme-ov-file#usage

#### 対処
`fetch-depth`を`2`に変更

### Google Blog API posts.insertリクエスト送信時403エラー
```log
<HttpError 403 when requesting https://blogger.googleapis.com/v3/blogs/***/posts?isDraft=true&alt=json returned "We're sorry, but you don't have permission to access this resource.". Details: "[***'message': "We're sorry, but you don't have permission to access this resource.", 'domain': 'global', 'reason': 'forbidden'***]">
```
#### 原因
Service Accountでは記事を投稿する権限はなかった。。。

#### 対処
なし、、、HTMLファイルをリポジトリの保存して、それをGoogle Bloggerに手動で更新することとする？
