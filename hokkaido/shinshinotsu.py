import requests
from bs4 import BeautifulSoup
import os
import re

# 対象のURLを指定
url = "https://www.vill.shinshinotsu.hokkaido.jp/hotnews/detail/00000288.html"
# 保存先のパス
save_path = ""
# URLにアクセスしてHTMLデータを取得
response = requests.get(url)
html_data = response.text

# BeautifulSoupを使用してHTMLをパース
soup = BeautifulSoup(html_data, "html.parser")

# 正規表現を使用して.pdfで終わるhref属性を持つaタグを取得
pdf_links = soup.find_all("a", href=re.compile(r'\.pdf$'))

# ベースURLを設定
base_url = "https://www.vill.shinshinotsu.hokkaido.jp/"

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


pdf_files = [] #　下のforで取得したpdf_file名を保存しておくリスト(50行)

#　PDFファイルをダウンロードして保存
for link in pdf_links:
    pdf_relative_url = link["href"]
    pdf_absolute_url = base_url + pdf_relative_url  # ベースURLと相対URLを結合
    pdf_file = os.path.basename(pdf_absolute_url)  # ファイル名を取得
    pdf_files.append(pdf_file)
    pdf_year = int(pdf_file[:4])
    pdf_wareki = convert_wareki(pdf_year)#　和暦に変える
    response = requests.get(pdf_absolute_url)

    tr_tag = link.find_parent("tr")#　aタグの親要素にあたるtrを取得
    if tr_tag:
        spans = tr_tag.find_all("span") #　trタグ内のspanタグを取得
        meeting_info = spans[0].get_text()  #　第n会　定例会　など

    
    #　議決結果と一般質問が存在していたとき spans[1]が議決結果　spans[2]が一般質問
    if len(spans) >= 3: 
        for item in pdf_files:
            if pdf_file[:8] == item[:8]: 
                pdf_info = spans[2].get_text()
            else:
                pdf_info = spans[1].get_text()
    elif len(spans) == 2: 
        pdf_info = spans[1].get_text()
    else:
        pdf_info = link.get_text()

    if response.status_code == 200:
        pdf_file_path = os.path.join(save_path,"新篠津村" + pdf_wareki + meeting_info + pdf_info + ".pdf")
        with open(pdf_file_path, "wb") as pdf:
            pdf.write(response.content)
            print(f"ダウンロード完了: {pdf_file}")
    else:
        print(f"ダウンロードエラー: {pdf_absolute_url}")
