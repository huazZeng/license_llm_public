import os

def read_files_to_map(directory):
    """
    将目录下所有 txt 文件的内容读取到一个字典中，键是文件名，值是文件内容。
    """
    files_map = {}

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件是否是 txt 文件
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            idx= filename.split('.')[0]
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 读取文件内容并存储到字典
                    content = file.read()
                    files_map[content] = idx
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    
    return files_map

def main():
    directory = r'src\llm_rag\queries'  # 请根据需要修改文件夹路径
    
    # 获取文件夹下所有 txt 文件的内容映射
    files_map = read_files_to_map(directory)
    print(files_map)
    # 打印文件名和文件内容的映射
    # for filename, content in files_map.items():
    #     print(f"File: {filename}")
    #     print(f"Content: {content[:100]}...")  # 打印文件内容的前100个字符，避免过长
    #     print("-" * 40)
    query_texts_default = ['distribute(reproduce) original or modified derivative works', 
                                    "use contributors' names, trademarks or logos", 
                                    'place warranty',
                                    'retain or copy the copyright notice in all copies or substantial uses of the work', 
                                    'include or duplicate the full text of license in modified software',
                                    'include that NOTICE when you distribute if the library has a NOTICE file with attribution notes',
                                    'disclose your source code when you distribute the software and make the source for the library available',
                                    ' state significant changes made to software', 'distribute copies of the original software or instructions',
                                    'give explicit credit or acknowledgement to the author with the software', 
                                    'change software name as to not misrepresent them as the original software', 
                                    'modify the software and creating derivatives', 
                                    'get permission from author or contact the author about the module you are using',
                                    'include the installation information necessary to modify and reinstall the software', 
                                    'compensate the author for any damages cased by your work', 'pay the licensor after a certain amount of use', 
                                    'use for commercial purpose or charge a fee', 
                                    'add other licenses with the software',
                                    'hold the author responsible or liable for subsequent impacts', 
                                    'practice patent claims of contributors to the code', 
                                    'sublicense: incorporate the work into things under terms of a more restrictive license', 
                                    'the library being compiled into the program linked at compile time rather than runtime', 
                                    'use or modify software freely without distributing it']
    
if __name__ == "__main__":
    main()
