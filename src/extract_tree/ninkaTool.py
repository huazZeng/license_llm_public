from .scantool import ScanTool
import subprocess
import re
import os

class NinkaScanTool(ScanTool):
    def initial(self, file_path: str) :
        return 
    
    def scan_file_license(self, file_path: str) -> str:
        """
        使用 Ninka 扫描文件的许可证信息。
        """
        try:
            result = subprocess.run(
                ['ninka', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0:
                license = result.stdout.strip()
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

    def scan_file_generateGoodSentense(self, file_path: str) -> str:
        """
        使用 Ninka 扫描文件并生成中间结果或适合的句子。
        """
        try:
            result = subprocess.run(
                ['ninka', '-i', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error scanning file: {result.stderr.strip()}"
        except Exception as e:
            return f"Exception occurred while scanning file: {str(e)}"
    def append_goodsentence_onTree(self, node):
        
            path = node.name+".goodsent"
            file = open(path, 'r')
            try:
                node.goodsent=file.read()
                ##TODO:check whether the context is meanningful
            except UnicodeDecodeError as e:
                print(f"this file is not in utf-8 type: {e}")
                node.goodsent='None'
            try:
                paths=[node.name+".badsent",node.name+".comments",
                    node.name+".goodsent",node.name+".license",node.name+".sentences",node.name+".senttok",]
                    
                for p in paths:
                    os.remove(p)
                    # print(f"File {p} has been deleted successfully.")
            except FileNotFoundError:
                print(f"File not found: {p}")
            except PermissionError:
                print(f"Permission denied: {p}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            
                
   