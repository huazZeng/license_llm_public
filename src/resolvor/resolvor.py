


import csv
from enum import Enum
from config import Attitude,license_terms
import json 
from extract_tree import extractor

def conflict_insite_parse(conflict,childlist):
    
    return [childlist[conflict[0]],license_terms[conflict[1]+1]]


def int_tree_to_attitude_list(int_tree):
    attitude_list = []
    
    for num in int_tree:
        # 将整数转换为二进制字符串，去掉 "0b" 前缀，保证是三位
        binary_str = bin(num)[2:].zfill(4)
        
        # 初始化当前节点的态度集合
        current_attitude = []
        
        # 检查二进制数的每一位
        if binary_str[0] == '1':  # 最高位表示 MUST
            current_attitude.append(Attitude.MUST)
        if binary_str[1] == '1':  # 第二位表示 CAN
            current_attitude.append(Attitude.CAN)
        if binary_str[2] == '1':  # 第三位表示 CANNOT
            current_attitude.append(Attitude.CANNOT)
        if binary_str[3] == '1':
            current_attitude.append(Attitude.NOMENTIONED)
        # 将当前态度加入列表
        attitude_list.append(current_attitude)
    
    return attitude_list    

def conflict_insite(license_result,limits_list):
    conflict = []
    for idx_child,limit in enumerate(limits_list):
        limit = int_tree_to_attitude_list(limit)
        for item_idx,attitude in enumerate(license_result):
            if license_result[item_idx] not in limit:
                conflict.append((idx_child,item_idx))
    return conflict
def limitfromitem(item):
        if item == Attitude.MUST:
            return 0b1100
        elif item==Attitude.CAN:
            return 0b1110
        elif item==Attitude.CANNOT:
            return 0b1001
        else:
            return 0b1111
def getLimitsFromlicenseresult(result):
        limit=[]
        for result_item in result:
            limit.append(limitfromitem(result_item))
        return limit
def conbine_lists(lists):
        """
        有多个列表 ，取列表中对应位置各个元素的交集，最后合并列表
        输出结果
            limits_conbined 交集后的列表,
            format_limit 交集后的列表的格式化结果,
            dependency_conflicts 冲突结果,输出为元组（i,j,index）,i,j为列表的索引，index为元素的索引，若ij超过了列表长度，则是与文本声明的许可证冲突
        
        """
        limits_conbined = []
        dependency_conflicts = []
        
        if len(lists) == 0:
            return [15]*23,int_tree_to_attitude_list([15]*23),[]
        else:
            for i in range(0,int(len(lists[0]))):
                result = 0b1111
                for j in range(0,len(lists)):
                    result = result & lists[j][i]
                limits_conbined.append(result)
                ## 如果结果为0 说明依赖不兼容，启动依赖兼容性的检测
                if result == 0b0000:
                    dependency_conflict = dependency_uncapable(lists,i)
                    dependency_conflicts.append(dependency_conflict)
            format_limit=int_tree_to_attitude_list(limits_conbined)
        return limits_conbined,format_limit,dependency_conflicts


def dependency_uncapable(self,lists,index):
    """
    依赖不兼容的情况
    """
    conflict = []
    for i in range(0,len(lists)):
        for j in range(i + 1,len(lists)):
            if lists[i][index] & lists[j][index] == 0b0000:
                conflict.append((i,j,index))
    return conflict    

def conflictparse(conflict,childlist):
    
    return [childlist[conflict[0]],childlist[conflict[1]],license_terms[conflict[2]+1]]

def conflict2print(conflict,isdependency):
    if isdependency:
        return f"dependency conflict: dependency {conflict[0]} is uncompatible with dependency {conflict[1]} on {license_terms[conflict[2]+1]} terms   "
    else :
        return f"file conflict: file {conflict[0]} is uncompatible with file {conflict[1]} on {license_terms[conflict[2]+1]} terms   "  
class resolvor:
    def __init__(self,root,c_r_output_file = "./conflict_resolution_result.json",conflict_output_file="./conflicts_insite.json"):
        self.root = root
        self.conflictnodes = []
        self.log={}
        self.declared_path2license = {}
        self.declared_path2licenseResult = {}
        self.declared_path2limits={}
        self.dependency_conflict = False
        self.GetGlobalDeclaredLicense(self.root)
        self.path2rlimits={}
        self.dependency_uncompatible = False
        self.dependency_conflicts_count = 0
        self.file_confilt_Count = 0
        self.confilt_issue_count = 0
        ## 添加依赖限制
        self.appendDependencyLimitOnNode(self.root)
        
        ## 传播限制
        self.appendlimitondir(self.root)
        
        self.printResult(self.root)
        self.save_results_to_json(self.root, c_r_output_file,conflict_output_file)
        print(f"this project has {self.dependency_conflicts_count} dependency conflicts and {self.file_confilt_Count} file conflicts")
        
        
        
        
    


    

    
   
    
    def saveResult(node, results):
        '''
        保存结果到json文件
        node: 节点
        results: 最后导入json的结果
        '''
        if not hasattr(node, 'Detectedlicenses'):
            if hasattr(node, 'replaced_licenses') and node.replaced_licenses is not None:
                if 'replaced_licenses' not in results:
                    results['replaced_licenses'] = []
                
                results['replaced_licenses'].append({
                    "name": node.name,
                    "replaced_licenses": node.replaced_licenses
                })
            if hasattr(node, 'replaced_license_result') :
                if 'replaced_license_result' not in results:
                    results['replaced_license_result'] = []
                    
                results['replaced_license_result'].append({
                    "name": node.name,
                    "replaced_license_result": extractor.license_result_serialize(node.replaced_license_result)
                })
            if hasattr(node, 'resolutions') and len(node.resolutions) != 0:
                if 'resolutions' not in results:
                    results['resolutions'] = []
                results['resolutions'].append({
                    "name": node.name,
                    "resolutions": [extractor.license_result_serialize(license_result) for license_result in node.resolutions] 
                })
            if hasattr(node, 'conflicts') and len(node.conflicts) != 0:
                if 'conflicts' not in results:
                    results['conflicts'] = []
                results['conflicts'].append({
                    "name": node.name,
                    "conflicts": [conflict_insite_parse(conflict,node.limitspath) for conflict in node.conflicts]
                })
                
            if hasattr(node,"conflicts_insite") and len(node.conflicts_insite) != 0:
                if 'conflicts_insite' not in results:
                    results['conflicts_insite'] = []
                results['conflicts_insite'].append({
                    "name": node.name,
                    "conflicts_insite": [conflict_insite_parse(conflict,node.limitspath) for conflict in node.conflicts_insite]
                })
            for child in node.children:
                resolvor.saveResult(child, results)
        else:
            if hasattr(node, 'replaced_licenses') and node.replaced_licenses is not None:
                
                if 'replaced_licenses' not in results:
                    results['replaced_licenses'] = []
                results['replaced_licenses'].append({
                    "name": node.name,
                    "replaced_licenses": node.replaced_licenses
                })
            if hasattr(node, 'replaced_license_result') :
                if 'replaced_license_result' not in results:
                    results['replaced_license_result'] = []
                    
                results['replaced_license_result'].append({
                    "name": node.name,
                    "replaced_license_result": extractor.license_result_serialize(node.replaced_license_result)
                })
            if hasattr(node, 'resolutions') and len(node.resolutions) != 0:
                if 'resolutions' not in results:
                    results['resolutions'] = []
                results['resolutions'].append({
                    "name": node.name,
                    "resolutions": [extractor.license_result_serialize(license_result) for license_result in node.resolutions] 
                })
            if hasattr(node, 'conflicts') and len(node.conflicts) != 0:
                if 'conflicts' not in results:
                    results['conflicts'] = []
                results['conflicts'].append({
                    "name": node.name,
                    "conflicts": [conflict_insite_parse(conflict,node.dependencys) for conflict in node.conflicts]
                })
            if hasattr(node,"conflicts_insite") and len(node.conflicts_insite) != 0:
                if 'conflicts_insite' not in results:
                    results['conflicts_insite'] = []
                results['conflicts_insite'].append({
                    "name": node.name,
                    "conflicts_insite": [conflict_insite_parse(conflict,node.dependencys) for conflict in node.conflicts_insite]
                })
    def save_results_to_json(self,root_node, c_r_output_file,conflict_output_file):
        results = {}
        results['file_conflict_count'] = self.file_confilt_Count
        results['dependency_conflict_count'] = self.dependency_conflicts_count
        results['dependency_uncompatible'] = self.dependency_uncompatible
        results['conflict_issue_count'] = self.confilt_issue_count
        resolvor.saveResult(root_node, results)
        if "conflicts_insite" in results:
            conflictdata = results['conflicts_insite']
        else:
            conflictdata = []
        with open(conflict_output_file, 'w', encoding='utf-8') as file:
            json.dump(conflictdata, file, ensure_ascii=False, indent=4)
            
        with open(c_r_output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"结果已保存到 {c_r_output_file} ,{conflict_output_file}")

    # 调用示例
    # save_results_to_json(root_node, 'output.json')

    def GetGlobalDeclaredLicense(self,node):
        '''
        获取全局声明的许可证
        获取声明式许可证的所有内容
        '''
        
        for idx,declared_path in enumerate(node.declared_licenses_path):
            if declared_path not in self.declared_path2license:
                self.declared_path2license[declared_path] = node.declared_licenses[idx]
                self.declared_path2licenseResult[declared_path] = node.declared_licenses_result[idx]
                
        for child in node.children:
            self.GetGlobalDeclaredLicense(child)
            
    def printResult(self,node):
        '''
            输出部分关键信息
        '''
        
        if not hasattr(node, 'Detectedlicenses'):
           
            if hasattr(node, 'replaced_licenses') and node.replaced_licenses != None:
               print(node.name)
               print(node.replaced_licenses)
               print("----------")
            if hasattr(node, 'conflicts') and len(node.conflicts) != 0:
                self.file_confilt_Count +=1
                print(node.name)
                print(conflict2print(conflictparse(node.conflicts),False))
                print("----------")
            for child in node.children:
                self.printResult(child)
        else:
            
            if hasattr(node, 'replaced_licenses') and node.replaced_licenses != None:
               print(node.name)
               print(node.replaced_licenses)
               print("----------")
            if hasattr(node, 'conflicts') and len(node.conflicts) != 0:
                self.dependency_conflict = True
                self.dependency_conflicts_count +=1
                print(node.name)
                print(conflict2print(conflictparse(node.conflicts,True)))
                print("----------")
            
    
    
    
    # 目前解决策略 根据不同情况来决定当前节点的比较
    # 根据比对结果生成可替换的许可证，而后的情况在可替换的许可证中选取
    # def resolve(self,node):
    #     if not hasattr(node, 'Detectedlicenses'):
    #         # 当前节点没有declaredlicense
    #         if node.parent != None and len(node.declared_licenses_result) == len(node.parent.declared_licenses_result):
    #             node.replacelicense=[]
                
    #         else:
    #             # 前面的declaredlicense被替代的情况
    #             if len(node.parent.replacelicense)>0:
    #                 self.license_compare(node.parent.replacelicense[0],node.declared_licenses_result[-1])
    #             # 前面declaredlicense未被替代的情况
    #             else:
    #                 self.license_compare(node.declared_licenses_result[-2],node.declared_licenses_result[-1])
                    
        
    #         for i in node.children:                                   
    #             self.resolve(i)
    #     else:
    #         if node.licenseresult == None:
    #             for depedencylicenseresult in node.dependencys_licenses_result:
    #                 self.license_compare(node.declared_licenses_result[-1],depedencylicenseresult)
                
    #         else:
    #             for depedencylicenseresult in node.dependencys_licenses_result:
    #                 self.license_compare(node.licenseresult,depedencylicenseresult)
    #             self.license_compare(node.declared_licenses_result[-1],node.licenseresult)
            
    
                
    def appendDependencyLimitOnNode(self,node):
        """
        通过文件节点的依赖许可证，为当前文件的最低级许可证添加限制
        """
        
        
        # 如果是文件夹节点，递归调用
        if not hasattr(node, 'Detectedlicenses'):
            for n in node.children:
                self.appendDependencyLimitOnNode(n)
                
                
        # 如果是文件节点
        else:
            limits = []
            # 获取所有依赖的许可证
            for idx,dependency_result in enumerate(node.dependencys_licenses_result):
                limit = getLimitsFromlicenseresult(dependency_result)
                

                limits.append(limit)
            
            
                
            # 合并依赖许可证 并生成limits
            limits_conbined,format_limit,dependency_conflicts = conbine_lists(limits)
            
            
            ## 如果存在冲突 直接返回即可 无法修复 输出结果 让用户处理
            if  len(dependency_conflicts) > 0:
                
                node.limits = limits_conbined
                node.conflicts = dependency_conflicts
                node.format_limits = format_limit   
                return 
            
            
            
            new_limit = limits_conbined
            ## 如果当前文件中的许可证与依赖冲突，直接在此处修复
            if node.license_result!=None: 
               
                # 给出修复方案
                resolutions,resolution = self.resolve_license(format_limit,node.license_result)
                node.resolutions = resolutions
                
                # 如果存在解决方案
                if resolution:
                    
                    
                    node.replaced_license_result = resolution['license_result']
                    node.replaced_licenses = resolution['license']
                    if resolution['license_result'] != None:
                        

                        node.conflicts_insite = conflict_insite(node.license_result,limits)

                        new_limit = getLimitsFromlicenseresult(node.replaced_license_result)
                        format_limit = int_tree_to_attitude_list(new_limit)
                
                
                
            node.limits = new_limit
            node.conflicts = dependency_conflicts
            node.format_limits = format_limit               
        
        
        
                
    def spread_upwards(self,node):
        if not hasattr(node, 'Detectedlicenses'):
            limits=[]
            limitspath=[]
            limitsnode=[]
            node.uncompatiblefile = []
            for n in node.children:
                if n == None:
                    break
                if n.conflicts != None and len(n.conflicts)>0:
                    node.uncompatiblefile.append(n.name)
                    continue
                if n.name.split('/')[-1].strip() == 'LICENSE':
                    continue
                
                limits.append(n.limits)
                limitspath.append(n.name)
                 
                
            limits_conbined,format_limit,file_conflicts = conbine_lists(limits)
            
            new_limit = limits_conbined
            
            if node.declared_license_insite != None and len(file_conflicts) == 0:
                resolutions,resolution = self.resolve_license(format_limit,node.declared_license_insite_result)
                node.resolutions = resolutions
                
                if resolution:
                    
                    
                    node.replaced_license_result = resolution['license_result']
                    node.replaced_licenses = resolution['license']
                    
                    if resolution['license_result'] != None:  
                        node.conflicts_insite = conflict_insite(node.declared_license_insite_result,limits)
                        new_limit = getLimitsFromlicenseresult(node.replaced_license_result)
                        format_limit = int_tree_to_attitude_list(new_limit)
            
            if len(file_conflicts) >0 :
               self.fix_fileconflict(file_conflicts)     
                
                
            node.limits = new_limit
            node.conflicts = file_conflicts
            node.format_limits = format_limit    
            node.limitspath = limitspath
            self.path2rlimits[node.name] = format_limit
            
            
            
            
        else:
            pass           
        
        ## 通过自顶向下逐步修复，
        # 如果是文件则查看是否有许可证 是否是文件许可证冲突，若不是则是依赖冲突 无法修复
        # 如果是文件夹则查看是否有许可证 如果没有许可证还需要逐步判断是与哪个文件冲突
    def fix_fileconflict(self,file_conflicts):
        return
    
    
    def appendlimitondir(self,node):
        if not hasattr(node, 'Detectedlicenses'):
            for n in node.children:
                if hasattr(n, 'Detectedlicenses'):   
                    continue
                else:
                    self.appendlimitondir(n) 
            self.spread_upwards(node) 
                      
    
    
    #默认license_result_p为父节点
    def license_compare(self,license_result_p,license_result_c):
        conflicts={}
        for index,attitude in enumerate(license_result_p):
            conflictReason = self.uncompatibleReason(attitude,license_result_c[index])
            if(conflictReason):
                conflicts[index]=conflictReason
            
        return conflicts
    
        
    
    
    
            
    ##对存在许可证的地方 进行解决算法
    ## limits为format_limit 是一个列表
    def resolve_license(self,limits,license_result):
        '''
            对于有矛盾的地方，进行修复
            最后返回结果： resolutions,best_resolution
            resolutions所有解决方案
            best_resolution 最佳解决方案，其中包含许可证名称，许可证态度，许可证异同程度
            
            如果没有矛盾，则返回的结果为 resolutions = [] ,best_resolution = {}
        '''
        
        conflict = []
        
        for idx,limit in enumerate(limits):
            if license_result[idx] in limit:
                continue
            else:
                conflict.append((idx,limits[idx]))
        if len(conflict) > 0:
            self.confilt_issue_count += 1
            resolutions,best_resolution = self.GetSolution(conflict,license_result,limits)
        else:
            resolutions = []
            best_resolution = {
            }
        return resolutions,best_resolution
    
    
    def GetSolution(self, conflict, license_,limit):
    # List to store all possible resolution strategies
        resolutions = []

        # Recursive function to generate all possible licenses
        def generate_licenses(license_, conflict_index):
            if conflict_index == len(conflict):
                # If all conflicts are processed, add the current license to resolutions
                resolutions.append(license_.copy())
                return

            # Get the current conflict
            idx, limit = conflict[conflict_index]

            # Try each possible value in the limit for the current conflict
            for item in limit:
                # Modify the license at the current conflict index
                license_[idx] = item
                # Recursively process the next conflict
                generate_licenses(license_, conflict_index + 1)

        # Start generating licenses from the first conflict
        generate_licenses(list(license_).copy(), 0)

        # Now, evaluate each resolution and find the best one
        replaced_licenses = []
        
        for new_license in resolutions:
            # Search for the best solution based on the new license
            solution = self.SearchSolution(new_license,limit,license_)
            replaced_licenses.append(solution)

        # Find the license with the minimum difference
        
        best_license = min(replaced_licenses, key=lambda x: x['difference'])
        if best_license['license'] == None:
            best_license['license'] = 'customer'
            best_license['license_result'] = resolutions[0]
            
        return resolutions,best_license
        
        
    ## 从数据库中查询解决方案    
    def SearchSolution(self, resolution,limits,license):
        # 将 resolution 转换为数字列表
        resolution_number = [x.value for x in resolution]
        license_number = [x.value for x in license]
        limits_number = [[x.value for x in limit] for limit in limits]
        # 读取 CSV 文件
        with open('Data/license_number_result.csv', 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        # 初始化最小差异值和最相似的行
        min_differences = float('inf')  # 初始化为无穷大
        most_similar_row = None
        most_similar_license = None
        
        # 遍历 CSV 文件的每一行
        for row in data[1:]:
            # 第一列是 license 的名字，后面的列是特征
            license_name = row[0]
            row_features = row[1:]
            
            # 将当前行的特征值转换为整数
            row_numbers = list(map(int, row_features))
            
            # 检查当前行的许可证是否符合限制
            if not  self.checklicense(row_numbers,limits) :
               continue
            
            # 计算当前行与 resolution_number 的差异数量
            differences = sum(1 for a, b in zip(row_numbers, license) if a != b)
            
            # 如果当前行的差异更小，则更新最相似的行
            if differences < min_differences:
                min_differences = differences
                most_similar_row = row_numbers
                most_similar_license = license_name
        
        # 返回结果
        return {
            'difference': min_differences,
            'license': most_similar_license,
            'license_result': most_similar_row
        }
         
         
    def checklicense(self,license,limit):   
        for i in range(0,len(license)):
            if license[i] not in limit[i]:
                return False
        return True
    def uncompatibleReason(self,attitude_p,attitude_c):
        if attitude_c==Attitude.MUST and (attitude_p == Attitude.CAN or attitude_p==Attitude.CANNOT or attitude_p==Attitude.NOMENTIONED) :
            return (attitude_c,attitude_p)
        ## 当子节点的态度为 can 父节点的态度不能为cannot
        elif attitude_c==Attitude.CAN and (attitude_p == Attitude.CANNOT):
            return (attitude_c,attitude_p)
        ## 当子节点态度为cannot 父节点态度必须为cannot
        elif attitude_c==Attitude.CANNOT and (attitude_p == Attitude.CAN or attitude_p==Attitude.MUST or attitude_p==Attitude.NOMENTIONED):
            return  (attitude_c,attitude_p)
        else:
            return None     
    
   
        
if __name__ == '__main__':
     
    print(conbine_lists([getLimitsFromlicenseresult([Attitude.MUST,Attitude.CAN,Attitude.CANNOT])]))
    