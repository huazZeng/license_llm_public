# import csv

# license_terms = {
#     1: ("Distribute", "Distribute original or modified derivative works", "Rights"),
#     2: ("Modify", "Modify the software and create derivatives", "Rights"),
#     3: ("Commercial Use", "Use the software for commercial purposes", "Rights"),
#     4: ("Relicense", "Add other licenses with the software", "Rights"),
#     5: ("Hold Liable", "Hold the author responsible for subsequent impacts", "Rights"),
#     6: ("Use Patent Claims", "Practice patent claims of contributors to the code", "Rights"),
#     7: ("Sublicense", "Incorporate the work into something that has a more restrictive license", "Rights"),
#     8: ("Statically Link", "The library can be compiled into the program linked at compile time rather than runtime", "Rights"),
#     9: ("Private Use", "Use or modify software freely without distributing it", "Rights"),
#     10: ("Use Trademark", "Use contributors’ names, trademarks or logos", "Rights"),
#     11: ("Place Warranty", "Place warranty on the software licensed", "Rights"),
#     12: ("Include Copyright", "Retain the copyright notice in all copies or substantial uses of the work.", "Obligations"),
#     13: ("Include License", "Include the full text of license in modified software", "Obligations"),
#     14: ("Include Notice", "Include that NOTICE when you distribute if the library has a NOTICE file with attribution notes", "Obligations"),
#     15: ("Disclose Source", "Disclose your source code when you distribute the software and make the source for the library available", "Obligations"),
#     16: ("State Changes", "State significant changes made to software", "Obligations"),
#     17: ("Include Original", "Distribute copies of the original software or instructions to obtain copies with the software", "Obligations"),
#     18: ("Give Credit", "Give explicit credit or acknowledgement to the author with the software", "Obligations"),
#     19: ("Rename", "Change software name as to not misrepresent them as the original software", "Obligations"),
#     20: ("Contact Author", "Get permission from author or contact the author about the module you are using", "Obligations"),
#     21: ("Include Install Instructions", "Include the installation information necessary to modify and reinstall the software", "Obligations"),
#     22: ("Compensate for Damages", "Compensate the author for any damages caused by your work", "Obligations"),
#     23: ("Pay Above Use Threshold", "Pay the licensor after a certain amount of use", "Obligations")
# }
# import csv

# # with open('Data/license_result_filtered.csv', 'r') as f:
# #     reader = csv.reader(f)
# #     data = list(reader)
# #     print(data[0])
# # # 删除空列
# # filtered_data = []
# # for row in data:
# #     filtered_row = [col for col in row if col.strip()]  # 去除空字符串
# #     filtered_data.append(filtered_row)

# # # 如果需要保存过滤后的数据到新文件
# # with open('Data/license_result_filtered.csv', 'w', newline='') as f:
# #     writer = csv.writer(f)
# #     writer.writerows(filtered_data
# import pandas as pd

# # 定义映射关系
# mapping = {
#     'must': 1,
#     'can': 2,
#     'cannot': 3,
#     'NOmentioned': 4
# }

# # 读取CSV文件
# df = pd.read_csv('Data\license_result_filtered.csv')

# # 将特征值转换为数字
# df.replace(mapping, inplace=True)

# # 保存转换后的CSV文件
# df.to_csv('converted_file.csv', index=False)

# print("转换完成，结果已保存到 'converted_file.csv'")


# import csv

# def process_csv(input_path, output_path):
#     with open(input_path, newline='', encoding='utf-8') as infile, \
#          open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)

#         for row in reader:
#             if row:  # 确保行非空
#                 first_col = row[0]
#                 parts = first_col.split("___")  # 按 "___" 拆分

#                 if len(parts) > 1:  
#                     second_part = parts[1]  # 取第二部分
#                 else:
#                     second_part = ""  # 若无第二部分，填空
#                 second_part = second_part.replace("-license", "")  
#                 row.insert(1, second_part)  # 插入到第二列

#                 writer.writerow(row)  # 写入处理后的行




# # 调用函数
# process_csv("Data\license_number_result.csv", "Data\license_spdx.csv")
import random

with open('Data\library_license.txt', mode='r', newline='', encoding='utf-8') as f:
    data = f.readlines()
    result = []
    for line in data:
        result.append(line.split(' ::::: ')[0])
    print(result)

with open('Data\library_selected.txt', mode='w', newline='', encoding='utf-8') as f:
    for line in result:
        I = random.random()
        if I >0.98:
            f.write(line + '\n')