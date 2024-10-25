import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# 假設你有一個電子商務商品名稱的數據集
data = {
    'product_name': [
        '蘋果手機殼',
        '蘋果筆記型電腦',
        '手機充電器',
        '三星筆記型電腦',
        '華為手機保護套'
    ]
}

# 將商品名稱放入一個 Pandas DataFrame 中
items_df = pd.DataFrame(data)

# 定義一個基於 jieba 的分詞函數
def jieba_tokenizer(text):
    return jieba.lcut(text)

# 創建 TfidfVectorizer，並指定 tokenizer 為 jieba_tokenizer
tfidf = TfidfVectorizer(tokenizer=jieba_tokenizer, ngram_range=(1, 2))

# 將商品名稱轉換為 TF-IDF 特徵矩陣
items_tfidf_matrix = tfidf.fit_transform(items_df['product_name'])

# 打印詞彙表
print("詞彙表:", tfidf.get_feature_names_out())

# 打印 TF-IDF 特徵矩陣
print("TF-IDF 特徵矩陣:")
print(items_tfidf_matrix.toarray())
