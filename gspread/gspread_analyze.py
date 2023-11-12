import gspread

# categorizeでurlから割り出した検索システムが、人手によるものと比較したときの一致率を判定

# Google Sheetsの認証
gc = gspread.service_account(filename="")  # サービスアカウントキーのJSONファイル

# スプレッドシートを開く
spreadsheet = gc.open("1788自治体会議録システム表 のコピー")
worksheet = spreadsheet.get_worksheet(1)

# 列番号指定
column9 = 9 
column10 = 10  

# 9列目と10列目のデータを取得
data_9 = worksheet.col_values(column9)
data_10 = worksheet.col_values(column10)

# カテゴリーごとの一致率を計算
def calculate_accuracy(data_9, data_10):
    matching_counts= {"Voices": 0, "Discuss": 0, "DBsearch": 0, "Sophia": 0, "sophia":0}
    
    for d9, d10 in zip(data_9, data_10):
            if "Voices" in d9 and "Voices" in d10:
                matching_counts["Voices"] += 1
            elif "Discuss" in d9 and "Discuss" in d10:
                matching_counts["Discuss"] += 1
            elif "DBsearch" in d9 and "DBsearch" in d10:
                matching_counts["DBsearch"] += 1
            elif "Sophia" in d9 and "Sophia" in d10:
                matching_counts["Sophia"] += 1
            elif "sophia" in d9 and "Sophia" in d10:
                matching_counts["sophia"] += 1
    return matching_counts

# カテゴリーごとの一致率を計算
matching_counts = calculate_accuracy(data_9, data_10)

# カテゴリーごとの一致率を表示
for category, matching_count in matching_counts.items():
    total_count_category = data_9.count(category)
    if total_count_category == 0:
        accuracy = 0.0
    else:
        accuracy = (matching_count / total_count_category) * 100
    print(f"{category}の一致率: {accuracy:.2f}% (マッチングカウント: {matching_count}/{total_count_category})")
