import gspread

#　会議録url内の文字から検索システムを判別

# Google Sheetsの認証
gc = gspread.service_account(filename="")  # サービスアカウントキーのJSONファイル

# スプレッドシートを開く
spreadsheet = gc.open("1788自治体会議録システム表 のコピー")
worksheet = spreadsheet.get_worksheet(1)
url_column = 12
data_url = worksheet.col_values(url_column)

#　会議録urlに指定の単語を含む場合、検索システムの名称を返す
def classify_category(url):
    if "voices" in url or "VOICES" in url or "gijiroku.com" in url:
        return "Voices" 
    elif "tenant" in url or "kensaku" in url or "www.gijiroku" in url or "www.kaigiroku.net" in url:
        if "kensakusystem" in url:
            return "Sophia"
        else:
            return "Discuss"
    elif "dbsr" in url or "db-search" in url:
        return "DBsearch"
    elif "ensakusystem" in url :
        return "Sophia"
    return "なし"

# 各URLを分析してカテゴリーに分類し、結果をリストに保存
categories = [classify_category(url) for url in data_url]

# カテゴリーの結果を8列目に書き込む
worksheet.update("J1:J" + str(len(categories)), [[category] for category in categories])

