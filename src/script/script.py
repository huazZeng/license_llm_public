import csv
import subprocess
import re
import os
from extract_tree import extractor
from  anytree import Node
def getlicensecontext(csv_file_name):
    
    with open(csv_file_name, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for row in csv_reader:
            licensename=row[0]
            print(f"{row[0]}")

def scanlicense(directory,csv_file_name):
    with open(csv_file_name, 'w',encoding='utf-8') as output_csvfile:
        csv_writer = csv.writer(output_csvfile)
       
          
        for item in os.listdir(directory):
            row=[]
            item_path = os.path.join(directory, item)
            row.append(item)
            ninka_output = scan_file(item_path)
            row.append(ninka_output)
            csv_writer.writerow(row)
        
               
def scan_file(file_path):
        try:
            result = subprocess.run(['ninka', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            if result.returncode == 0:
                license=result.stdout.strip()
                match = re.search(r';([^;]+)', license)
                if match:
                    license_result = match.group(1)
                else:
                    license_result = 'NONE'
                return license_result
            else:
                return f"Error scanning file: {result.stderr.strip()}"
        except Exception as e:
            return f"Exception occurred while scanning file: {str(e)}"


# directory_to_scan = 'ninka/t/data/licenses'
# root = Node(directory_to_scan)
# extractor.build_tree(directory_to_scan, root)
# extractor.generate_goodsentence_basedonTree(root)
# extractor.append_goodsentence_onTree(root)
#     # print_tree_with_ninka_output(root)
# jsoncontext=extractor.tree_to_json(root)
# with open('license_llm/Data/license-can-result.json', 'w') as f:
#     f.write(jsoncontext)
# print("数据已写入 license-can-result.json 文件")
import os
import csv

# 指定文件夹路径
folder_path = 'ninka/t/data/licenses'

# 指定输出CSV文件的路径
output_csv_path = 'output.csv'

# 创建或覆盖CSV文件
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
    # 创建CSV写入器
    csv_writer = csv.writer(csv_file)
    
    # 写入CSV文件的标题行
    csv_writer.writerow(['Name', 'Content'])
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 确保是文件而不是文件夹
        if os.path.isfile(file_path):
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 写入文件名和内容到CSV
            csv_writer.writerow([filename, content])

print(f"所有文件已成功提取到CSV文件：{output_csv_path}")