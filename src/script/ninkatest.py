from extract_tree.extract_tree import extractor
from anytree import Node
import difflib
import Levenshtein
import numpy as np
def licensematch(sent1,path):
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        context=file.read()
    matcher = difflib.SequenceMatcher(None, sent1, context)
    similarity = matcher.ratio()
    return similarity            

# directory_to_scan = '/home/zhz/ninka/t/data/licenses'
# root = Node(directory_to_scan)
    
# extractor.build_tree(directory_to_scan, root)
    
# extractor.generate_goodsentence_basedonTree(root)
# extractor.append_goodsentence_onTree(root)
# jsoncontext=extractor.tree_to_json(root)
# with open('ninkarepolicensetree.json', 'w') as f:
#         f.write(jsoncontext)
import json

# 读取文件内容
with open('ninkarepolicensetree.json', 'r') as f:
    json_content = f.read()

# 将内容解析为 JSON 格式
json_data = json.loads(json_content)


match_SequenceMatcher=[]
match_Levenshtein=[]
match_Levenshtein_distance=0
count=0
unknowncount=0
nonecount=0
known=0
for child in json_data['children']:
    match_SequenceMatcher.append(licensematch(child['goodsent'],child['name'])) 
    match_Levenshtein.append(Levenshtein.ratio(child['goodsent'], child['name'])) 
    count+=1
for child in json_data['children']:
    if child['ninka_output'] == 'UNKNOWN':
        unknowncount+=1
    elif child['ninka_output'] == 'NONE':
        nonecount+=1
    else:
        known+=1
        print(child['ninka_output'],child['name'])
    
median_valueSequenceMatcher = np.median(match_SequenceMatcher)

# 计算平均数
mean_valueSequenceMatcher = np.mean(match_SequenceMatcher)

median_valueLevenshtein = np.median(match_Levenshtein)

# 计算平均数
mean_valueLevenshtein = np.mean(match_Levenshtein)
print(f"unknowncount : {unknowncount} ;nonecount:{nonecount} ; knowncount={known}")
print(f"match_SequenceMatcher  Median:{median_valueSequenceMatcher} Mean: {mean_valueSequenceMatcher}")
# print(f"match_Levenshtein Median:{median_valueLevenshtein} Mean: {mean_valueLevenshtein} ")
