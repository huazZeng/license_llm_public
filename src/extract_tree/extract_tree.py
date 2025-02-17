import os
import subprocess
from anytree import Node
import json
import re
import pickle
from .dependencyTool import dependencyTool
from .licenseanalysis import LicenseAnalyser
from .scantool import ScanTool
from .ninkaTool import NinkaScanTool
from .scancodetool import scancodetool
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
    
class extractor:
    def __init__(self,scantool,dependency_tool,directory):
        self.scantool = scantool
        
        self.dependency_tool = dependency_tool
        self.dependency_tool.initial(directory)
        self.scantool.initial(directory)
        
    def scan_file_license(self,file_path):
        return self.scantool.scan_file_license(file_path)
        
    ## Use ninka to scan the file and output  result and the Intermediate file.  
    ## comments filter(?)
    # def scan_file_with_ninka_generateGoodSentense(file_path):
    #     try:
    #         result = subprocess.run(['ninka','-i', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    #         if result.returncode == 0:
    #             return result.stdout.strip()
    #         else:
    #             return f"Error scanning file: {result.stderr.strip()}"
    #     except Exception as e:
    #         return f"Exception occurred while scanning file: {str(e)}"    





    ## scan dependencies in files
    # def scan_file_dependencies(file_path):
    #     dependencies = []
    #     file_extension = os.path.splitext(file_path)[1]
    #     language = detect_language(file_extension)
    #     if language and language in patterns:
    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             for line in file:
    #                 match = patterns[language].match(line)
    #                 if match:
    #                     dependency = match.group(1) or match.group(2)
    #                     if dependency and dependency.split('.')[0] not in dependencies:
    #                         dependencies.append(dependency.split('.')[0])  # 只取顶级模块名
    #                         # print(getlicense('a16e675410f6baa826341cc6e028c227',dependency.split('.')[0],'pypi'))
    #     return dependencies

    # build the tree including information about license and dependency
    def build_tree(self,directory, parent_node):
        
        
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item).replace('\\', '/')
            ##忽略git文件夹
            if os.path.isdir(item_path) :
                if item not in ignore_dirs:
                    dir_node = Node(item_path, parent=parent_node)
                    self.build_tree(item_path, dir_node)
            else:
                #所有叶节点都是文件
               
                dependencys_licenses=[]
                file_node = Node(item_path, parent=parent_node)
                file_node.item_name=item
                ## TODO dependencies
                dependencys=self.dependency_tool.extract_dependencies(item_path)
                
                ## TODO dependencies license
                for dependency in dependencys:
                    dependencys_licenses.append(self.dependency_tool.get_license(dependency))
                    
                
                
                
                    
                # TODO diverse tools
                   
                Detectedlicenses = self.scantool.scan_file_license(item_path)
                file_node.dependencys = dependencys
                file_node.Detectedlicenses = Detectedlicenses
                file_node.dependencys_licenses=dependencys_licenses
                
    # get the sentence about License            
    def generate_goodsentence_basedonTree(self,node):             
        if hasattr(node, 'Detectedlicenses'):
            self.scantool.scan_file_generateGoodSentense(node.name)
        else :
            for child in node.children:
                self.generate_goodsentence_basedonTree(child)
                
    def append_goodsentence_onTree(self,node):
        if hasattr(node, 'Detectedlicenses'):
            node.goodsent = self.scantool.append_goodsentence_onTree(node.name)
        else :
            for child in node.children:
                self.append_goodsentence_onTree(child)


    def appendlicenseresult(self,node):
        if hasattr(node, 'Detectedlicenses'):
            dependencys_licenses_result=[]
            license=node.Detectedlicenses
            goodsent=node.goodsent
            license_result=LicenseAnalyser.license_Analys(license,goodsent)
            node.license_result=license_result
            dependencys_licenses=node.dependencys_licenses
            
            
            if len(dependencys_licenses) !=0 :           
                for dependencys_license in dependencys_licenses:
                    
                    dependencys_licenses_result.append(LicenseAnalyser.dependencie_license_Analys(dependencys_license))
                    
            node.dependencys_licenses_result=dependencys_licenses_result
        else :
            for child in node.children:
                self.appendlicenseresult(child)
    
       
    def print_tree_with_Detectedlicenses(node, indent=""):
        print(f"{indent}{node.name}")
        if hasattr(node, 'Detectedlicenses'):
            for line in node.Detectedlicenses.split('\n'):
                print(f"{indent} {'ninka_result:'}  {line}")
        if hasattr(node,'dependencys'):
            print(f"{indent} {'dependencys:'} {node.dependencys}")
        if hasattr(node,'goodsent'):
            print(f"{indent} {'goodsent:'}   {node.goodsent}")
        if hasattr(node,'declared_licenses'):
            print(f"{indent} {'declared_licenses:'}   {node.declared_licenses}")

        for child in node.children:
            extractor.print_tree_with_Detectedlicenses(child, indent + "    ")
            
    def license_result_serialize(license_result):
        return [x.name for x in license_result]
            
    #TODO:reconstruction
    def node_to_dict(node):
        node_dict = {'name': node.name}
        if hasattr(node, 'license_result') and node.license_result is not None:
            node_dict['license_result'] = extractor.license_result_serialize(node.license_result)
        if hasattr(node, 'dependencys_licenses_result') and node.dependencys_licenses_result is not None:
            node_dict['dependencys_licenses_result'] =[extractor.license_result_serialize(license_result) for license_result in node.dependencys_licenses_result] 
        if hasattr(node, 'Detectedlicenses') and node.Detectedlicenses is not None:
            node_dict['Detectedlicenses'] = node.Detectedlicenses
        if hasattr(node, 'declared_licenses_result') and node.declared_licenses_result is not None:
            node_dict['declared_licenses_result'] = [extractor.license_result_serialize(license_result) for license_result in node.declared_licenses_result]
        if hasattr(node, 'dependencys') and node.dependencys is not None:
            node_dict['dependencys'] = node.dependencys
            
        if hasattr(node, 'goodsent') and node.goodsent is not None:
            node_dict['goodsent'] = node.goodsent
        if hasattr(node, 'dependencys_licenses') and node.dependencys_licenses is not None:
            node_dict['dependencys_licenses'] = node.dependencys_licenses    
        if hasattr(node, 'declared_licenses') and node.declared_licenses is not None:
            node_dict['declared_licenses'] = list(node.declared_licenses)
        if hasattr(node,"limits") and node.limits is not None:
            node_dict['limits'] = node.limits
        if hasattr(node, 'format_limits') and node.format_limits is not None:
            node_dict['format_limits'] = [extractor.license_result_serialize(license_result) for license_result in node.format_limits]     
        if hasattr(node, 'declared_licenses_path') and node.declared_licenses_path is not None:
            node_dict['declared_licenses_path'] = list(node.declared_licenses_path)
        
            
        if hasattr(node, 'children'):
            node_dict['children'] = [extractor.node_to_dict(child) for child in node.children]
        else:
            node_dict['children'] = []

        return node_dict       
    def tree_to_json(self,node):
        return json.dumps(extractor.node_to_dict(node), indent=4)


    # add the the declared licenses 项目许可证或者覆盖文件夹的许可证
    # 目前在叶子节点也加上了declared项，并且涵盖由上至下所有declared，便于修改
    def append_declared_licenses_onTree(self,parent_node):
        if not hasattr(parent_node, 'Detectedlicenses'):
            parent_node.declared_licenses=set()
            
            parent_node.declared_licenses_path=set()
            parent_node.declared_licenses_result=set()
            
            parent_node.declared_license_insite=None
            parent_node.declared_license_insite_result=None
            
            if parent_node.parent != None:
                for license in parent_node.parent.declared_licenses:
                    parent_node.declared_licenses.add(license)
                
                for declared_licenses_result in parent_node.parent.declared_licenses_result:
                    parent_node.declared_licenses_result.add(declared_licenses_result)
                    
                for declared_licenses_path in parent_node.parent.declared_licenses_path:
                    parent_node.declared_licenses_path.add(declared_licenses_path)
                    
            for child in parent_node.children:
                if hasattr(child, 'Detectedlicenses') and child.item_name == 'LICENSE':
                    
                    
                    # #在此处先进行字符级别的匹配 没有再用ninka的结果
                    with open(f'{parent_node.name}/LICENSE') as file:
                        context=file.read()
                    # matchresult=LicenseAnalyser.license_match(context)
                    # if matchresult != None:
                    #     result = tuple(LicenseAnalyser.license_Analys(matchresult,context))
                    #     parent_node.declared_license.add(matchresult)
                        
                    #     parent_node.declared_license_insite=matchresult
                    #     parent_node.declared_license_result=result
                        
                        
                    #     parent_node.declared_licenses_path.add(parent_node.name)
                    #     parent_node.declared_licenses_result.add(result)
                    #     # 保持LICENSE文件被分析时与在declaredlicense中内容是一致的
                    #     child.Detectedlicenses = matchresult
                    #     child.goodsent = context
                    # else:
                    result = tuple(LicenseAnalyser.license_Analys(child.Detectedlicenses,context))
                        
                    parent_node.declared_license_insite=child.Detectedlicenses
                    parent_node.declared_license_insite_result=result
                    parent_node.declared_licenses.add(child.Detectedlicenses)

                    child.goodsent = context
                    parent_node.declared_licenses_result.add(result)
                  
                self.append_declared_licenses_onTree(child)
        else:
            parent_node.declared_licenses=set()


            parent_node.declared_licenses_result=set()
            parent_node.declared_licenses_path=set()
            
            for license in parent_node.parent.declared_licenses:
                parent_node.declared_licenses.add(license)
                
            for declared_licenses_result in parent_node.parent.declared_licenses_result:
                parent_node.declared_licenses_result.add(declared_licenses_result)
                
            for declared_licenses_path in parent_node.parent.declared_licenses_path:
                parent_node.declared_licenses_path.add(declared_licenses_path)
                
                
                
# if __name__ == "__main__":
#     directory_to_scan = '/home/zhz/repo/hackingtool'
#     root = Node(directory_to_scan)
    
#     extractor.build_tree(directory_to_scan, root)
    
#     extractor.generate_goodsentence_basedonTree(root)
#     extractor.append_goodsentence_onTree(root)
#     extractor.append_declared_licenses_onTree(root)
#     # print_tree_with_ninka_output(root)
#     jsoncontext=extractor.tree_to_json(root)
#     with open('tree.json', 'w') as f:
#         f.write(jsoncontext)
#     print("数据已写入 tree.json 文件")
#     # 使用 pickle 将字典打包成字节序列
#     byte_data = pickle.dumps(jsoncontext)

#     # 将字节序列写入文件
#     with open('data.pkl', 'wb') as file:
#         file.write(byte_data)

#     print("数据已写入 data.pkl 文件")