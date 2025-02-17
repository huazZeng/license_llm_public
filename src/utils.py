import csv
import difflib  # 用于相似度计算
from extract_tree import LicenseAnalyser


def getresult(license, similarity_threshold=0.8):
    best_match = None  # 存储最相似的一行
    max_similarity = 0  # 记录最高相似度

    # 读取 CSV 文件
    with open('Data\license_spdx.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)  # 读取所有行

    # 统一大小写
    license_lower = license.lower()
    
    for row in data:
        if not row:  # 跳过空行
            continue
        first_col = row[1].strip().lower()  # 取第一列并去除空格
        
        # 计算相似度
        similarity = difflib.SequenceMatcher(None, first_col, license_lower).ratio()

        # 只存储相似度最高的行，并确保超过阈值
        if similarity >= similarity_threshold and similarity > max_similarity:
            print(first_col)
            best_match = row[2:]
            max_similarity = similarity

    # 如果找到匹配项，则进行数据转换
    if best_match:
        
        print(best_match)
        result = [LicenseAnalyser.number2attitude(value) for value in best_match]
        return result

    return None  # 没有匹配返回 None

print(getresult("MIT"))