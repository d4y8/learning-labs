import os
import glob

from googleapiclient.discovery import build

#必要なスコープを指定
# SCOPES = ["https://www.googleapis.com/auth/blogger"] 

service = build("blogger", "v3")

# ブログIDを指定
blog_id = os.environ.get("BLOG_ID")

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

                # listは権限あり
                # results = service.posts().list(blogId=blog_id).execute()
                # print(results)

                # 403エラー
                result = service.posts().insert(blogId=blog_id).execute()
                print(result)

        except UnicodeDecodeError:
            print(f"Error: Encoding error in {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
