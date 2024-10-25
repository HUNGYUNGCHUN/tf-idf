import pandas as pd

# 完整的檔案路徑，包括資料夾和檔案名稱
file_path = 'results'

# 讀取 CSV 檔案
df = pd.read_csv(file_path)

# 排序並選出前 100 個搜尋詞
sorted_df = df.sort_values(by='results_count', ascending=False)
top_100_search_terms = sorted_df.head(100)

# 印出結果或儲存
print(top_100_search_terms)
top_100_search_terms.to_csv('/path/to/your/folder/top_100_search_terms.csv', index=False)
