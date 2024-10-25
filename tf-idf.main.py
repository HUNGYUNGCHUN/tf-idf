import os
import pandas as pd
import pickle
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# 停用詞列表
stop_words = set(["的", "是", "在", "了", "和"])  # 可根據需求添加更多停用詞

# 自定義 jieba 分詞函數
def jieba_tokenizer(text):
   text = re.sub(r"[^\w\s]", "", text)  # 去除特殊符號
   words = jieba.lcut(text)
   return [word for word in words if word not in stop_words]  # 過濾停用詞

# 指定合併產品的 CSV 檔案與 TF-IDF 檔案
output_file = 'merged_data.csv'
tfidf_pickle_file = 'tfidf_matrix.pkl'
vectorizer_pickle_file = 'tfidf_vectorizer.pkl'

# 合併 CSV 檔案
if os.path.exists(output_file):
   print(f"檔案 '{output_file}' 已經存在，讀取資料中...")
   merged_df = pd.read_csv(output_file)
else:
   merged_df = pd.DataFrame()  # 假設已經合併好的資料
   # 此處添加合併 CSV 檔案的邏輯（例如，讀取多個 CSV 檔案並合併）
   merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')

# 檢查 TF-IDF 是否已存在
if os.path.exists(tfidf_pickle_file) and os.path.exists(vectorizer_pickle_file):
   print("從 pickle 讀取 TF-IDF 資料...")
   with open(tfidf_pickle_file, 'rb') as f:
       tfidf_matrix = pickle.load(f)
   with open(vectorizer_pickle_file, 'rb') as f:
       tfidf_vectorizer = pickle.load(f)
else:
   print("開始計算 TF-IDF matrix...")
   tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenizer)
   tfidf_matrix = tfidf_vectorizer.fit_transform(merged_df['product_name'].astype(str))
   
   # 保存 TF-IDF 結果
   with open(tfidf_pickle_file, 'wb') as f:
       pickle.dump(tfidf_matrix, f)
   with open(vectorizer_pickle_file, 'wb') as f:
       pickle.dump(tfidf_vectorizer, f)

# 讀取查詢詞的 txt 檔案
query_terms = []

with open('top250.txt', 'r', encoding='utf-8-sig') as file:
   for line in file:
       line = line.strip()
       if line:  # 確保行不為空
           query_terms.append(line)  # 將查詢詞添加至列表

# 顯示讀取的查詢詞
print("查詢詞:")
for query in query_terms:
   print(query)

# 設定相似度門檻值
threshold = 0.1
top_k = 10  # 設定固定的 top_k 值

# 儲存所有查詢結果的 DataFrame
all_results = pd.DataFrame()

# 依次搜尋每個查詢詞並輸出結果到資料夾
for query_term in query_terms:
   print(f"搜尋查詢詞：{query_term}")
   
   # 將查詢詞轉換成 TF-IDF 向量
   query_vector = tfidf_vectorizer.transform([query_term])
   
   # 計算餘弦相似度
   cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
   
   # 過濾出相似度大於閾值的產品
   filtered_indices = [i for i, score in enumerate(cosine_similarities) if score > threshold]
   similar_products = merged_df.iloc[filtered_indices].copy()
   
   # 加入相似度分數
   similar_products['similarity_score'] = cosine_similarities[filtered_indices]
   
   # 去除重複產品
   similar_products_deduplicated = similar_products.drop_duplicates(subset='product_name', keep='first')
   
   # 根據相似度排序並取前 top_k 個結果
   similar_products_sorted = similar_products_deduplicated.sort_values(by='similarity_score', ascending=False).head(top_k)
   
   # 顯示當前查詢詞的相似產品數量
   print(f"查詢詞 '{query_term}' 的相似產品數量: {len(similar_products_sorted)}")
   
   # 如果沒有找到相似產品，填充空行
   num_rows = 10  # 每個查詢詞需要滿足的行數

   if len(similar_products_sorted) < num_rows:
       # 創建一個填充行
       empty_rows = pd.DataFrame({
           'product_name': [None] * (num_rows - len(similar_products_sorted)),
           'similarity_score': [None] * (num_rows - len(similar_products_sorted)),
           '序列': [None] * (num_rows - len(similar_products_sorted)),
           '查詢詞': [query_term] * (num_rows - len(similar_products_sorted))
       })
       
       # 將結果合併
       similar_products_sorted = pd.concat([similar_products_sorted, empty_rows], ignore_index=True)

   # 將序列編號加入結果
   similar_products_sorted['序列'] = range(1, len(similar_products_sorted) + 1)

   # 添加查詢詞欄位
   similar_products_sorted['查詢詞'] = query_term

   # 合併到所有結果
   all_results = pd.concat([all_results, similar_products_sorted], ignore_index=True)

# 替換空值為 '字元'
all_results.fillna('.', inplace=True)

# 檢查所有結果
print("最終結果的列:")
print(all_results.columns)
print("最終結果的筆數:", len(all_results))

# 保存所有查詢結果至一個 CSV 檔案
final_output_filename = "tf_df_results_250.csv"
all_results.to_csv(final_output_filename, index=False, encoding='utf-8-sig')

print(f"所有查詢結果已保存至 '{final_output_filename}'")
print("所有查詢完成！")
