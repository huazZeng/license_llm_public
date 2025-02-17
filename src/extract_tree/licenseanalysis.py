
from anytree import Node
from enum import Enum
import difflib
import csv
from llm_rag import QueryProcessor
from llm_rag import RAGProcessor
from config import Attitude
class LicenseAnalyser:
    
                
    ## 此处插入RAG llm 与 许可证比对
    def license_Analys(license,goodsent):
        if license == 'None':
            return None
        elif license == 'NONE':
            return None
        elif license == 'UNKNOWN':
            #先做文本比对（？）
            licensename=LicenseAnalyser.license_match(goodsent)
            if licensename == None:
                return LicenseAnalyser.llm_analys(goodsent)
            else:
                return  LicenseAnalyser.getresult(licensename)  
        else:
            ## 是否存在预先处理好的许可证信息 无的话进行识别
            result = LicenseAnalyser.getresult(license)
            if result==None:
                return LicenseAnalyser.llm_analys(goodsent)
            return  result
    
    
    def dependencie_license_Analys(goodsent)    :
        print(goodsent)
        if goodsent == 'NONE':
            return  [Attitude.NOMENTIONED]*23
        result = LicenseAnalyser.getresult(goodsent)
        if result == None:
            return LicenseAnalyser.llm_analys(goodsent)
        else:
            return result
        
    import csv
    import difflib  



    def getresult(license, similarity_threshold=0.8):
        best_match = None  # 存储最相似的一行
        max_similarity = 0  # 记录最高相似度

        # 读取 CSV 文件
        with open('Data\license_spdx.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)  # 读取所有行

        # 统一大小写
        license_lower = license.lower()
        
        for row in data[1:]:
            if not row:  # 跳过空行
                continue
            first_col = row[1].strip().lower()  # 取第一列并去除空格
            
            # 计算相似度
            similarity = difflib.SequenceMatcher(None, first_col, license_lower).ratio()

            # 只存储相似度最高的行，并确保超过阈值
            if similarity >= similarity_threshold and similarity > max_similarity:
                # print(first_col)
                best_match = row[2:]
                max_similarity = similarity

        # 如果找到匹配项，则进行数据转换
        if best_match:
            
            # print(best_match)
            result = [LicenseAnalyser.number2attitude(value) for value in best_match]
            return result

        return None  # 没有匹配返回 None


    def number2attitude(number):
        
    
        if number == '1':
            return Attitude.MUST
        elif number == '2':
            return Attitude.CAN
        elif number == '3':
            return Attitude.CANNOT
        elif number == '4':
            return Attitude.NOMENTIONED    
    def license_match(goodsent):
        ##在数据库中做文本比对，得到可能的结果
        with open('Data/licensecontent.csv', mode='r', newline='', encoding='utf-8') as csv_file:
            mostsimilarity=0
            licensename=''
            reader = csv.reader(csv_file)
            for row in reader:
                similarity=LicenseAnalyser.compare_strings(row[1],goodsent)
                if(similarity>mostsimilarity):
                    mostsimilarity=similarity
                    licensename=row[0]
            if(mostsimilarity>0.90):
                return    licensename
            else :
                return None
        
    
   

    def compare_strings(s1, s2):
        matcher = difflib.SequenceMatcher(None, s1, s2)
        similarity = matcher.ratio()
        return similarity 
    
    
    
    
    
    def llm_analys(goodsent):
        
        
        ragProcessor = RAGProcessor(goodsent)
        query_contents = ragProcessor.process_multiple_queries()
        query_processor = QueryProcessor()
            # 执行查询
        results = query_processor.process_all_queries(query_contents,ragProcessor.query_texts_default)
        
        
        
        
        
        
        
        return results
    

    
    
    
   
    
    
# with open('Data/licensecontent.csv', mode='r', newline='', encoding='utf-8') as csv_file:
    
#     reader = csv.reader(csv_file)
#     for row in reader:
#         # print(f"{row[0]},{row[1]}")
#         print(f"{row[0]},{LicenseAnalyser.license_match(row[1])}")
