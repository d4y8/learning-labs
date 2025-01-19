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
