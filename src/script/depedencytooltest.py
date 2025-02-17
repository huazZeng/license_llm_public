# 基于pipreqsnb可能存在扫描到内部模块的问题
# 而对于pipreqs不存在以上问题能否以此作为一个补充
from anytree import Node
from extract_tree import extractor
import subprocess
import os
import json
import re


ignore_dirs = [
        ".hg",
        ".svn",
        ".git",
        ".tox",
        "__pycache__",
        "env",
        "venv",
        ".ipynb_checkpoints",
]
patterns = {
    'python': re.compile(r'^\s*(?:from\s+(\S+)\s+import|import\s+(\S+))'),
    'javascript': re.compile(r'^\s*(?:require\(\s*["\'](\S+)["\']\s*\)|import\s+(\S+))'),
    'java': re.compile(r'^\s*import\s+(\S+);'),
    'cpp': re.compile(r'^\s*#\s*include\s+<(\S+)>')
}
def extract_dependencies_py(file_path):
        # 运行 pipreqs 命令并捕获输出
        file_extension = os.path.splitext(file_path)[1]
        language = detect_language(file_extension)
        if language == 'python':

            try:
                result = subprocess.run(['pipreqsnb', '--print', file_path],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                # 如果命令成功执行，可以处理输出
        
            except subprocess.CalledProcessError as e:
                print(f"An unexpected error occurred: {e}")
                result=''
            except Exception as e:
                # 捕获其他所有可能的错误
                print(f"An unexpected error occurred: {e}")
                result=''
            output=result.stdout.decode('utf-8')
            dependencies = re.findall(r'^\s*([\w\-]+)==([\d\.]+)\s*$', output, re.MULTILINE)
            
            # 格式化输出，生成完整的依赖项字符串
            formatted_dependencies = [f"{name}" for name, version in dependencies]

            # formatted_dependencies = "\n".join([f"{name}=={version}" for name, version in dependencies])
            return formatted_dependencies
        else:
            return []
    
    
def detect_language(file_extension):
        if file_extension in ['.py']:
            return 'python'
        elif file_extension in ['.js']:
            return 'javascript'
        elif file_extension in ['.java']:
            return 'java'
        elif file_extension in ['.cpp', '.h']:
            return 'cpp'
        return None
def scan_file_dependencies(file_path):
    dependencies = []
    file_extension = os.path.splitext(file_path)[1]
    language = detect_language(file_extension)
    if language and language in patterns:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = patterns[language].match(line)
                if match:
                    dependency = match.group(1) or match.group(2)
                    if dependency and dependency.split('.')[0] not in dependencies:
                        dependencies.append(dependency.split('.')[0]) 
    return dependencies

def build_tree(directory, parent_node,extract_dependencies_py):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
            ##忽略git文件夹
        if os.path.isdir(item_path) :
            if item not in ignore_dirs:
                dir_node = Node(item_path, parent=parent_node)
                build_tree(item_path, dir_node,extract_dependencies_py)
        else:
                #所有叶节点都是文件
            file_node = Node(item_path, parent=parent_node)
            file_node.item_name=item
            dependencys=extract_dependencies_py(item_path)
            file_node.dependencys = dependencys
   

def scan_repo_by(directory_to_scan,extract_dependencies_py,label):
    name=directory_to_scan.split('/')[-1]
    root = Node(directory_to_scan)
    build_tree(directory_to_scan, root,extract_dependencies_py)
    jsoncontext=extractor.tree_to_json(root)
    with open(f'/home/zhz/license_llm/Data/test/{name}_{label}.json', 'w') as f:
        f.write(jsoncontext)
    print(f"数据已写入 /home/zhz/license_llm/Data/test/{name}_{label}.json 文件")

def scanrepobypipreqs(file_path):
    result = subprocess.run(['pipreqs', '--print', file_path],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    output=result.stdout.decode('utf-8')
    dependencies = re.findall(r'^\s*([\w\-]+)==([\d\.]+)\s*$', output, re.MULTILINE)
    formatted_dependencies = [f"{name}" for name, version in dependencies]

    return formatted_dependencies

if __name__ == "__main__":
    with open 

    
    directory='/home/zhz/repo'
    items=['unstract','numpy','matplotlib','localstack','core','anytree','roop']
    for item in items:
        item_path = os.path.join(directory, item)
        try:
            scan_repo_by(item_path,scan_file_dependencies,'reg')
            scan_repo_by(item_path,extract_dependencies_py,'pipreqsnb')
        except SyntaxError as e:
            print(f"SyntaxError caught: {e}")
        except FileNotFoundError as e:
            print(f"FileNotFoundError : {e}")
        except Exception as e:
            # 捕获其他所有可能的错误
            print(f"An unexpected error occurred: {e}")
    
    directory='/home/zhz/repo'
    result={}
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        try:
            result[item_path] = scanrepobypipreqs(item_path)
       
        except Exception as e:
            print(f"Exception caught: {e}")
  
    with open(f'/home/zhz/license_llm/Data/test/pipreqs.json', 'w') as f:
        json.dump(result, f)
    print(f"数据已写入 /home/zhz/license_llm/Data/test/pipreqs.json 文件")
