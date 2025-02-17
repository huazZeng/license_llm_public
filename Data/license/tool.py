import csv

# 假设文本文件名为 'licenses.txt'
input_file_name = 'license_llm/Data/license/liresolver/library_license.txt'

output_file_name = 'licenses.csv'

# 读取文本文件并解析每一行
with open(input_file_name, 'r') as file:
    lines = file.readlines()

# 准备CSV内容
csv_lines = []
for line in lines:
    parts = line.strip().split(' ::::: ')
    if len(parts) == 2:
        project, license = parts
        csv_lines.append([project, license])

# 写入CSV文件
with open(output_file_name, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # 写入CSV标题
    csv_writer.writerow(['Project', 'License'])
    # 写入CSV数据
    csv_writer.writerows(csv_lines)

print(f"Data has been successfully written to {output_file_name}")