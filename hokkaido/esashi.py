import requests
from bs4 import BeautifulSoup
import os
import re

# 対象のURLを指定
url = "https://www.esashi.jp/gikai/meeting/minutes.html"
# 保存先のパス
save_path = "/Users/sakaguchi/Documents/my scrapings/hokkaido"
# URLにアクセスしてHTMLデータを取得
response = requests.get(url)
html_data = response.content

# BeautifulSoupを使用してHTMLをパース
soup = BeautifulSoup(html_data, "html.parser")  # エンコーディングを指定

# 正規表現を使用して.pdfで終わるhref属性を持つaタグを取得
pdf_links = soup.find_all("a", href=re.compile(r'\.pdf$'))

# ベースURLを設定
base_url = "https://www.esashi.jp"

# PDFファイルをダウンロードして保存
for link in pdf_links:
    pdf_relative_url = link["href"]
    pdf_absolute_url = base_url + pdf_relative_url  # ベースURLと相対URLを結合

    # ここから新しい部分
    pdf_file_text = link.get_text()  # aタグ内のテキストを取得

    response = requests.get(pdf_absolute_url)

    if response.status_code == 200:
        pdf_file_path = os.path.join(save_path, f"江差町_{pdf_file_text}.pdf")
        with open(pdf_file_path, "wb") as pdf:
            pdf.write(response.content)
            print(f"ダウンロード完了: {pdf_file_text}")
    else:
        print(f"ダウンロードエラー: {pdf_absolute_url}")
