import os
import glob
import httplib2

from googleapiclient.discovery import build
from oauth2client import file, client, tools

blogger_client_id = os.environ['blogger_client_id']
blogger_client_secret = os.environ['blogger_client_secret']


credential_path = 'credentials.json'  # 認証情報を保存するファイルパス

blog_id = os.environ.get("BLOG_ID")
blogger_post(blog_id=blog_id, title="test", contest="test")

def blogger_post(blog_id, title, content, labels, isDraft=True):
    if content is None:
        print('コンテンツがないため作成できません')
        return None

    # OAuth 2.0の認証フローを設定
    flow = client.OAuth2WebServerFlow(blogger_client_id, blogger_client_secret, 'https://www.googleapis.com/auth/blogger', redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    storage = file.Storage(credential_path)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage)

    # 認証情報を使用してBlogger APIを初期化
    http = credentials.authorize(httplib2.Http())
    service = build('blogger', 'v3', http=http)

    # 新しい投稿を作成するためのデータ
    post_data = {
        "kind": "blogger#post",
        "blog": {
            "id": blog_id
        },
        "title": title,
        "content": content,
        "labels": labels,
    }

    # 投稿を作成
    try:
        if isDraft:
            new_post = service.posts().insert(blogId=blog_id, body=post_data, isDraft=True).execute()
            print("新しい下書きが作成されました。投稿のID:", new_post['url'])
        else:
            new_post = service.posts().insert(blogId=blog_id, body=post_data).execute()
            print("新しい投稿が作成されました。投稿のID:", new_post['url'])
        return True
    except Exception as e:
        print("投稿の作成中にエラーが発生しました:", str(e))
        return False
    

# #必要なスコープを指定
# # SCOPES = ["https://www.googleapis.com/auth/blogger"] 

# service = build("blogger", "v3")

# # ブログIDを指定
# blog_id = os.environ.get("BLOG_ID")

# try:
#     directory = "html"
#     # ディレクトリ内のすべての.htmlファイルをリストアップ
#     html_files = glob.glob(os.path.join(directory, "*.html"))

#     if not html_files:
#         print(f"No HTML files found in '{directory}'.")
#         exit
#     for filepath in html_files:
#         try:
#             with open(filepath, "r", encoding="utf-8") as file:
#                 html_content = file.read()

#                 body = {
#                     "kind": "blogger#page",
#                     "content": html_content,
#                     "title": "Title"
#                 }

#                 # listは権限あり
#                 results = service.posts().list(blogId=blog_id).execute()
#                 print(results)

#                 # insertは403エラー
#                 result = service.posts().insert(blogId=blog_id).execute()
#                 print(result)

#         except UnicodeDecodeError:
#             print(f"Error: Encoding error in {filepath}")
#         except Exception as e:
#             print(f"Error processing {filepath}: {e}")

# except Exception as e:
#     print(f"An error occurred: {e}")
