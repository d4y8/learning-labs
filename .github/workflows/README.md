# GitHub Actions
基本的な[GitHub Docs](https://docs.github.com/ja/actions/about-github-actions)

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
作成したサービスアカウントキーの内容を、GitHubリポジトリのシークレットとして登録します。リポジトリの設定 > Secrets and variables > Actionsで、「New repository secret」をクリックし、キーの名前（例: GOOGLE_CREDENTIALS）と値（JSONキーファイルの内容）を入力して保存します。

## 

https://github.com/google-github-actions/auth

## TODO
- GitHub Actionsのワークフロー開発に使うエディタはVSCODEらしいけど、どう使う？？
- GitHub Actionsの構文理解
- Pythonの構文理解