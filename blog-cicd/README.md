# GitHub ActionsからGoogle Bloggerに完全自動ポストできるか検証する
## 結論から先に
Service Accountで認証する場合、Google Bloggerへポストする権限がなく、完全自動化はできない。

## 自動化しようとした背景
WordPressで運用していたブログをGoogle Bloggerにマイグレーションした際、
移行ツールはあるものの結構手間だった。特に画像の移行。
なので今後ブログサーバーの移行があっても楽できるように
ブログのリソース(記事、画像)はGitHubで管理、ついでに諸々自動化できたらというのが動機。

## やりたいこと
- ブログのリソース(記事や画像)はGitHubで管理したい。
- 記事はMarkdownで書きたい。
- リポジトリにPushしたらGitHub ActionsでBloggerに自動で投稿したい。

## 事前準備
Google Blogger APIを利用するにあたり、認証に必要な設定をしておく。

### Google Cloud設定
Google BloggerのアカウントでGoogle Cloudのプロジェクトは作成済みであることを前提とする。

#### Blogger APIの有効化
作成済みのGoogle Cloudのプロジェクトで、Blogger APIを有効する。
Google Cloud Consoleの[APIとサービス] > [ライブラリ]で[Blogger API]を検索。

<img src="./README-images/gc-api-library-google-blogger.png" width="80%">

有効にする。

<img src="./README-images/gc-api-library-google-blogger-describe.png" width="80%">

#### Service Accountの作成
GitHub ActionsからBlogger APIにアクセスするために、サービスアカウントを作成。

Google Cloud Consoleの[IAMと管理] > [サービスアカウント]で、新しいサービスアカウントを作成。

<img src="./README-images/gc-create-service-account.png" width="80%">

#### キーの作成

サービスアカウントの認証に使用するJSON形式のキーを作成。
Google Cloud Consoleのサービスアカウントの詳細ページで、[鍵]タブを選択し、
[キーを追加] > [新しい鍵を作成]を選択。キーのタイプは[JSON]を選択し[作成]。
キーファイルがダウンロードされる。

<img src="./README-images/gc-create-service-account-key.png" width="80%">

### GitHubリポジトリへのシークレット登録
作成したサービスアカウントキーの内容を、GitHubリポジトリのシークレットとして登録。
リポジトリの[Settings] > [Secrets and variables] > [Actions]で、[New repository secret]押下し、
[Name]と[Secret]（サービスアカウントキーファイルの内容）を入力して保存。

<img src="./README-images/github-secret-settings.png" width="80%">

## GitHub Actionsのワークフロー作成

### ざっくりとしたフロー
1. mainブランチへのプッシュで起動
1. Gitリポジトリをcheckout
1. commitしたmdをhtmlへ変換
1. Google Cloud認証
1. htmlをGoogle BloggerへPost

### md -> html変換
[pandoc](https://pandoc-doc-ja.readthedocs.io/ja/latest/users-guide.html)を利用する。

### GitHub Actions から Google Cloud への認証
[google-github-actions/auth](https://github.com/google-github-actions/auth?tab=readme-ov-file#service-account-key-json)でService Account Key Jsonでの認証を利用する。

### 実装内容
.github/workflows/insert-post-to-google-blogger.yaml
```yaml
name: Insert post to Google Blogger

on:
  push:
    branches: 
    - main
    paths:
    - '**/*.md'
    - '.github/**/*.*'
  workflow_dispatch:

jobs:
  call-blogger-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: 
          fetch-depth: 2
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13.1'
      - name: Install dependencies
        run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
      - name: Convert Markdown to HTML
        env:
            GITHUB_EVENT_BEFORE: ${{ github.event.before }}
            GITHUB_EVENT_REPOSITORY_URL: ${{ github.event.repository.url}}
        run: |
          set -eux
          sudo apt-get install -y pandoc

          diff_list=$(git diff --name-only ${GITHUB_EVENT_BEFORE}..HEAD)

          for file in $diff_list; do
            if [[ ${file} != *.md ]]; then
              continue
            fi
            
            dir_name=$(dirname ${file})
            html_dir=${dir_name}/html
            mkdir -p ${html_dir}

            # md -> html変換
            html_file=${html_dir}/$(basename "${file}" .md).html
            pandoc -f markdown -t html "${file}" > ${html_file}

            # img パス置換
            # ./README-images
            # ↓
            # https://github.com/d4y8/learning-labs/blob/main/<MARKDOWN_DIR_PATH>/README-images

            before_path="\.\/README-images"

            after_path="${GITHUB_EVENT_REPOSITORY_URL}/blob/main/${dir_name}/README-images"
            after_path=${after_path//\//\\/}
            after_path=${after_path//./\\.}
            after_path=${after_path//\?/\\\?}

            sed -i 's/'${before_path}'/'${after_path}'/g' ${html_file}

            before_string="\.png\""
            after_string="\.png\?raw=true\""

            sed -i 's/'${before_string}'/'${after_string}'/g' ${html_file}

            cat ${html_file}
          done

          git config user.name  "actions-user"
          git config user.email "action@github.com"
          git add .
          git commit -m "Converted Markdown to HTML"
          git push

      - name: Set up authentication
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GOOGLE_CREDENTIALS }}

      - name: Call Blogger API
        env: 
          BLOG_ID: ${{ secrets.BLOG_ID }}
        run: |
          python .github/scripts/blog_post.py

```

.github/scripts/blog_post.py
```py
import os
import glob

from googleapiclient.discovery import build

service = build("blogger", "v3")

# ブログIDを指定
blog_id = os.environ.get("BLOG_ID")

DIRECTORY_HTML = "html"
# ディレクトリ内のすべての.htmlファイルをリストアップ
html_files = glob.glob(os.path.join(DIRECTORY_HTML, "*.html"))

if not html_files:
    print(f"No HTML files found in '{DIRECTORY_HTML}'.")
    exit
for filepath in html_files:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            html_content = file.read()

            body = {
                "content": html_content,
                "title": "test title"
            }

            # listは権限あり
            # results = service.posts().list(blogId=blog_id).execute()
            # print(results)

            # insertは403エラー
            result = service.posts().insert(blogId=blog_id).execute()
            print(result)

    except UnicodeDecodeError:
        print(f"Error: Encoding error in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

```

### GitHub Actionsが実行されると、Bloggerへの投稿時に403エラー
エラー内容
```log
<HttpError 403 when requesting https://blogger.googleapis.com/v3/blogs/***/posts?alt=json returned "We're sorry, but you don't have permission to access this resource.". Details: "[***'message': "We're sorry, but you don't have permission to access this resource.", 'domain': 'global', 'reason': 'forbidden'***]">
```
#### 原因
Service AccountではGoogle Bloggerに記事を投稿する権限はない。

#### 対策(検討)
なし、、、HTMLファイルをリポジトリの保存して、それをGoogle Bloggerに手動更新する？

### 今後やれたら
Textlint、Google Search Console、SNSポスト辺りも自動化できたら良い。

## Troubleshooting
その他、発生したエラーと対処。

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

#### 解決方法
`fetch-depth`を`2`に変更

###　GitHub Actionsでgit push
```log
remote: Permission to d4y8/learning-labs.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/d4y8/learning-labs/': The requested URL returned error: 403
```
#### 原因
ワークフローにリポジトリに対して書き込み権限がないため

#### 解決方法
[Settings] > [Actions] > [General] > [Workflow permissions]
`Read and write permissions`を選択して[Save]。
