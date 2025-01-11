import os

from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/blogger"] #必要なスコープを指定
# SERVICE_ACCOUNT_FILE = "credentials.json" #credentials.jsonは不要。上記authアクションで認証が完了している。

service = build("blogger", "v3")

# ブログIDを指定
blog_id = os.environ.get("BLOG_ID")


# # 変更されたMDファイルを取得
# # ループ
#   # Blogerに投稿済みかチェック
#     # 投稿済みの場合
#       # Bloggerに投稿
#     # 投稿済みでない場合
#       # Bloggerに投稿


# 投稿リストを取得する例
results = service.posts().list(blogId=blog_id).execute()

print(results)