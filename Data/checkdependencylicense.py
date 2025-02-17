import csv
import requests



csv_file_name = 'license_llm/Data/license/licenses.csv'
output_csv_file_name='license_llm/Data/license/dependency_licenses.csv'



# 读取CSV文件
def get_license_pypi(package_name):
    url = f'https://pypi.org/pypi/{package_name}/json'
    
    # 发送请求
    response = requests.get(url)
    
    # 将响应内容转换为 JSON
    response_json = response.json()
    
    if 'message' not  in response_json: 
        license = response_json['info'].get('license', None)
    else:
        license ='NOMESSAGE'
    return license



with open(csv_file_name, 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    
    
    with open(output_csv_file_name, 'w', newline='', encoding='utf-8') as output_csvfile:
        output_csv_writer = csv.writer(output_csvfile)
        # 写入标题行
        output_csv_writer.writerow(headers)
        
        # 遍历输入CSV文件的每一行并写入输出CSV文件
        for row in csv_reader:
            row[1]=get_license_pypi(row[0])
            print(f"Project: {row[0]}, License: {row[1]}")
            if row[1]!='UNKNOWN':
                output_csv_writer.writerow(row)   
                 
