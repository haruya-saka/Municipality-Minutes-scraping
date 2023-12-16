import requests
from bs4 import BeautifulSoup
import os
import re

# 対象のURLを指定
url_dicision = "https://www.town.yakumo.lg.jp/site/gikai/list25.html"
url_record = "https://www.town.yakumo.lg.jp/site/gikai/list26.html"
# 保存先のパス
save_path = "/Users/sakaguchi/Documents/my scrapings/hokkaido"
# URLにアクセスしてHTMLデータを取得
response_d = requests.get(url_dicision)
html_data_d = response_d.content

response_r = requests.get(url_record)
html_data_r = response_r.content

# BeautifulSoupを使用してHTMLをパース
soup_r = BeautifulSoup(html_data_r, "html.parser")

# articleタグを取得
pdf_spans_r = soup_r.find_all("span", class_="article_title")

url_absolute = "https://www.town.yakumo.lg.jp"

term_link_list = []
minute_link_list = []

# 年号一覧からリンクを取得する処理
for span in pdf_spans_r:
    a_term = span.find("a")
    term_link = a_term.get("href")
    term = a_term.get_text()
    print(term)
    term_list_url = url_absolute + term_link
    term_dict = {"term": term, "url": term_list_url}
    term_link_list.append(term_dict)

print(term_link_list)
for term_dict in term_link_list:
    url = term_dict["url"]
    term = term_dict["term"]
    res = requests.get(url)
    html = res.content
    # ここでパースしたのが年号クリック先のページ
    soup = BeautifulSoup(html, "html.parser")
    # 定例会会議録、臨時会会議録などのスパンを取得
    minutes_link_spans = soup.find_all("span", class_="span_b article_title")
    for m_span in minutes_link_spans:
        # ここで会議種テキストを取得（定例会会議録、など）
        minutes_a = m_span.find("a")
        minute_link = minutes_a.get("href")
        minute_name = minutes_a.get_text()
        # print(minute_name, minute_link)
        minute_dict = {"name": minute_name, "url":url_absolute + minute_link}
        minute_link_list.append(minute_dict)
        
print(minute_link_list)
for link in minute_link_list:
    m_name = link["name"]
    res = requests.get(link["url"])
    html = res.content
    soup = BeautifulSoup(html, "html.parser")
    div_detail = soup.find("div", class_="detail_free")
    a_pdf = div_detail.find("a")
    pdf_link = a_pdf.get("href")
    pdf_name = a_pdf.get_text()
    print(m_name, pdf_name, pdf_link)