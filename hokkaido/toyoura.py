import requests
from bs4 import BeautifulSoup
import os
import re

# 対象のURLを指定
url = "https://www.town.toyoura.hokkaido.jp/hotnews/category/308.html"
# 保存先のパス
save_path = "Municipality-Minutes-scraping/pdf/toyoura"
# URLにアクセスしてHTMLデータを取得
response = requests.get(url)
html_data = response.content

# BeautifulSoupを使用してHTMLをパース
soup = BeautifulSoup(html_data, "html.parser")

# articleタグを取得
article_tag = soup.find("article", id="article")

# articleタグ内のaタグを取得
links = article_tag.find_all("a")

#　pdfの年から和暦に変換
def convert_wareki(year):
    era_table = {
        "明治": (1868, 1912),
        "大正": (1912, 1926),
        "昭和": (1926, 1989),
        "平成": (1989, 2019),
        "令和": (2019, 9999)
    }

    for era, (first, end) in era_table.items():
        if first <= year < end:
            wareki_year = year - first + 1
            wareki = f"{era}{wareki_year}年"
            return wareki
    return "元号なし"

# 取得したaタグを表示
for link in links:
    print(link["href"], link.text)
    response = requests.get(link["href"])
    html = response.content

    soup = BeautifulSoup(html, "html.parser")
    # articleタグを取得
    article_tag = soup.find("article", id="article")

    # articleタグ内のaタグを取得
    a_tags = article_tag.find_all("a")
    base_url = "https://www.town.toyoura.hokkaido.jp"
    # PDFファイルをダウンロードして保存
    for a_tag in a_tags:
        pdf_relative_url = a_tag["href"]
        pdf_absolute_url = base_url + pdf_relative_url  # ベースURLと相対URLを結合
        pdf_file = os.path.basename(pdf_absolute_url)  # ファイル名を取得
        pdf_year = int(pdf_file[:4])
        pdf_wareki = convert_wareki(pdf_year)#　和暦に変える
        response = requests.get(pdf_absolute_url)
        
        pdf_file_text = a_tag.get_text()  # aタグ内のテキストを取得

        response = requests.get(pdf_absolute_url)

        if response.status_code == 200:
            pdf_file_path = os.path.join(save_path, f"豊浦町{pdf_wareki}{pdf_file_text}.pdf")
            with open(pdf_file_path, "wb") as pdf:
                pdf.write(response.content)
                print(f"ダウンロード完了: {pdf_file_text}")
        else:
            print(f"ダウンロードエラー: {pdf_absolute_url}")
