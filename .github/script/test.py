import os

from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/blogger"] #必要なスコープを指定
# SERVICE_ACCOUNT_FILE = "credentials.json" #credentials.jsonは不要。上記authアクションで認証が完了している。

service = build("blogger", "v3")

# ブログIDを指定
blog_id = os.environ.get("BLOG_ID")

# 投稿リストを取得する例
results = service.posts().list(blogId=blog_id).execute()

print(results)