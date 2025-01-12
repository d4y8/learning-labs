import os
import glob
import json

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


# try:
#     with open("sample.html, "r", encoding="utf-8") as file:
#         content = file.read()
#         print(content)
# except FileNotFoundError:
#     print("ファイルが見つかりません。")
# except UnicodeDecodeError:
#     print("ファイルのエンコードがUTF-8ではありません。")


try:
    directory = "html"
    # ディレクトリ内のすべての.htmlファイルをリストアップ
    html_files = glob.glob(os.path.join(directory, "*.html"))

    if not html_files:
        print(f"No HTML files found in '{directory}'.")
        exit
    for filepath in html_files:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                html_content = file.read()

                body = {
                    "kind": "blogger#page",
                    "content": html_content,
                    "title": "Title"
                }

                # data = {}  # 空の辞書を作成
                # data['content'] = "test"
                # data['title'] = "Title"
                # data = {
                #         "kind": "blogger#page",
                #         "id": ddd,
                #         "status": ddd,
                #         "blog": {
                #             "id": blog_id
                #         },
                #         "published": datetime,
                #         "updated": datetime,
                #         "url": ddd,
                #         "selfLink": ddd,
                #         "title": ddd,
                #         "content": ddd,
                #         "author": {
                #             "id": ddd,
                #             "displayName": ddd,
                #             "url": ddd,
                #             "image": {
                #             "url": ddd
                #             }
                #         }
                #     }

                # body = json.dumps(data, ensure_ascii=False, indent=4) # JSON文字列に変換
                # body = json.dumps(data, ensure_ascii=False) # JSON文字列に変換
                # print(body)

                result = service.posts().insert(blogId=blog_id, body=body).execute()
                # result = service.posts().insert(blogId=blog_id).execute()
                print(result)
                # 例: ファイルの内容をそのまま出力
                # print(html_content)
        except UnicodeDecodeError:
            print(f"Error: Encoding error in {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

# # 投稿リストを取得する例
# results = service.posts().list(blogId=blog_id).execute()

# print(results)