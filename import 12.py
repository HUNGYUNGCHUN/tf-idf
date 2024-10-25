import os
import pandas as pd
import chardet

# 指定原始 CSV 檔案所在的資料夾路徑
source_folder_path = './results'

# 指定新的資料夾路徑
output_folder_path = './789'

# 確保新的資料夾存在，如果不存在則創建
os.makedirs(output_folder_path, exist_ok=True)

# 初始化一個清單來儲存每個 CSV 檔案的資料量
file_data = []

# 讀取資料夾中的所有 CSV 檔案
for file_name in os.listdir(source_folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(source_folder_path, file_name)
        
        # 檢測檔案的編碼
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            print(f'Detected encoding for {file_name}: {encoding}')

        try:
            # 嘗試讀取 CSV 檔案，使用檢測到的編碼
            df = pd.read_csv(file_path, encoding=encoding)
            
            # 確保 DataFrame 不是空的
            if not df.empty:
                # 計算該 CSV 檔案的資料量（行數）
                data_size = len(df)
                
                # 將檔案名稱和資料量加入清單
                file_data.append((file_name, data_size))
            else:
                print(f'Skipping empty file: {file_name}')
        
        except pd.errors.EmptyDataError:
            print(f'Skipping empty file: {file_name}')
        except Exception as e:
            print(f'Error reading {file_name}: {e}')

# 將資料量排序，選出前 100 個 CSV 檔案
sorted_files = sorted(file_data, key=lambda x: x[1], reverse=True)
top_100_files = sorted_files[:100]

# 為每個檔案輸出獨立的 CSV 檔案到新的資料夾
for file_name, data_size in top_100_files:
    original_file_path = os.path.join(source_folder_path, file_name)
    
    # 重新讀取檔案以便儲存
    with open(original_file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    
    # 讀取 CSV 檔案，使用正確的編碼
    df = pd.read_csv(original_file_path, encoding=encoding)
    
    # 為新的檔案名稱添加前綴
    output_file_name = f'top_100_{file_name}'
    output_file_path = os.path.join(output_folder_path, output_file_name)
    
    # 儲存結果到新的 CSV 檔案，使用 UTF-8 編碼
    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

# 印出確認訊息
print(f'Top 100 CSV files have been saved to {output_folder_path} with prefix "top_100_"')
