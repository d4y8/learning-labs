import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



API_SERVICE_NAME = "blogger"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/blogger"]
CLIENT_SECRETS_FILE = 'client_secrets.json'


def get_authenticated_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


if __name__ == "__main__":
    service = get_authenticated_service()

    body = {
        "kind": "blogger#page",
        "content": "test",
        "title": "Title"
    }

    blog_id = os.environ.get("BLOG_ID")
    # listは権限あり
    results = service.posts().list(blogId=blog_id).execute()
    print(results)

    # insertは403エラー
    result = service.posts().insert(blogId=blog_id).execute()
    print(result)




    # youtube.hoge() ... 動画を検索したり、アップロードしたり、再生リスト作ったり...
    # サンプルコード: https://developers.google.com/youtube/v3/code_samples?hl=ja#python

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
