import os

from googleapiclient.discovery import build

service = build("blogger", "v3")

# ブログIDを指定
blog_id = os.environ.get("BLOG_ID")

with open("html.txt", "r", encoding="utf-8") as f:
    html_files = f.read().splitlines()

for filepath in html_files:
    print(filepath)
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
            result = service.posts().insert(blogId=blog_id, contents=body).execute()
            print(result)

    except UnicodeDecodeError:
        print(f"Error: Encoding error in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
