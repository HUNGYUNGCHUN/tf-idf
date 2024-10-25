import os

# 指定原始 CSV 檔案所在的資料夾路徑
source_folder_path = './789'
# 指定輸出 TXT 檔案的路徑
output_txt_path = './output.txt'

# 初始化一個清單來儲存提取的字串
extracted_names = []

# 讀取資料夾中的所有 CSV 檔案
for file_name in os.listdir(source_folder_path):
    if file_name.endswith('.csv'):
        # 去掉 .csv 扩展名
        base_name = file_name[:-4]  # 去掉最后的四个字符（.csv）
        
        # 分割文件名，並檢查是否有至少四個部分
        parts = base_name.split('_')
        if len(parts) > 3:
            extracted_name = parts[3]  # 提取第三个下划线后的部分
            extracted_names.append(extracted_name)

# 將提取的字串寫入 TXT 檔案
with open(output_txt_path, 'w', encoding='utf-8') as f:
    for name in extracted_names:
        f.write(name + '\n')

# 印出確認訊息
print(f'Extracted names have been saved to {output_txt_path}')
