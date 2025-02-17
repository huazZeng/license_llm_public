import openai
import time
import json
from  enum import Enum
import os
from config import Attitude,license_terms


query2idx = {'Distribute original or modified derivative works': '1',
             "use contributors' names, trademarks or logos": '10', 
             'place warranty': '11',
             'retain or copy the copyright notice in all copies or substantial uses of the work': '12',
             'include or duplicate the full text of license in modified software': '13',
             'include that NOTICE when you distribute if the library has a NOTICE file with attribution notes': '14',
             'disclose your source code when you distribute the software and make the source for the library available': '15', 
             ' state significant changes made to software': '16',
             'distribute copies of the original software or instructions': '17',
             'give explicit credit or acknowledgement to the author with the software': '18',
             'change software name as to not misrepresent them as the original software': '19', 
             'modify the software and creating derivatives': '2',
             'get permission from author or contact the author about the module you are using': '20',
             'include the installation information necessary to modify and reinstall the software': '21',
             'compensate the author for any damages cased by your work': '22',
             'pay the licensor after a certain amount of use': '23',
             'use for commercial purpose or charge a fee': '3', 
             'add other licenses with the software': '4',
             'hold the author responsible or liable for subsequent impacts': '5',
             'practice patent claims of contributors to the code': '6',
             'sublicense: incorporate the work into things under terms of a more restrictive license': '7',
             'the library being compiled into the program linked at compile time rather than runtime': '8',
             'use or modify software freely without distributing it': '9'
             }

self_refine_prompt_path = "src\llm_rag\self_refine-prompt"
Rights=[]
Obligations=[]

import re

    
    
def extract_answer(final_answer):
    match = re.search(r"therefore, the answer is", final_answer, re.IGNORECASE)
    
    if match:
        try:
            answer_word = final_answer[match.end():].strip().split()[0].strip('.')
        except IndexError:
            answer_word = "Extraction error"
    else:
        fallback_match = re.findall(r'\b(can|must|cannot|nomentioned)\b', final_answer, re.IGNORECASE)
        if fallback_match:
            
            answer_word = fallback_match[-1].lower()
        else:
           
            answer_word = "Not found"
    
    return answer_word


class QueryProcessor:
    def __init__(self, api_key):
        openai.api_key = api_key
        
    def selfrefine(self,output_content,query):
        while(True):
            self_refine_file = os.path.join(self_refine_prompt_path, f"{query2idx[query]}.txt")
            if os.path.exists(self_refine_file):
                with open(self_refine_file, 'r', encoding='utf-8') as sr_file:
                    self_refine_content = sr_file.read()

            
                answer1 = self.process_query(output_content)
            
                time.sleep(2)

            
                second_prompt = self_refine_content + "\n" + \
                                "Here is the question:\n" + output_content + "\nGPT-4's initial answer was:\n" + answer1 + \
                                "\nNow, please reconsider the answer to the above question in combination with the initial example. " \
                                "You can stick to your judgment. The last sentence should be 'Therefore, the answer is ...', where '...' is among 'can'/'cannot'/'nomentioned'/'must'.\n"

                

                final_answer = self.process_query(second_prompt)
                answer_word =extract_answer(final_answer)

            else:
                output_content+= "The last sentence should be 'Therefore, the answer is ...', where '...' is among 'can'/'cannot'/'nomentioned'/'must'."
        
                

                answer = self.process_query(output_content)
                answer_word = extract_answer(answer)
            if(answer_word =="Not found" or answer_word =="Extraction error"):
                continue
            else :
               break
        print(answer_word)
        return answer_word
        
        
    def process_query(self, related_content):
        

        # 调用 GPT-4 模型
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": related_content},
            ]
        )
        return response.choices[0].message['content']

    def process_all_queries(self,related_contents,queries):
        """
        处理多条查询
        """
        results = []

        for idx, related_content in enumerate(related_contents):
            output_content = self.selfrefine(related_content,queries[idx])
            results.append(output_content)
            if idx % 3 == 1:
                time.sleep(60)
                

        self.results = results
        
        
        return self.process_result(results)
    
    def process_result(self,results,idx):
        format_results = []
        
        for idx,result in enumerate(results):
            if result == "can" :
                format_results.append(Attitude.CAN)
            elif result == "must":
                format_results.append(Attitude.MUST)
            elif result == "cannot" :
                format_results.append(Attitude.CANNOT)
            else :
                ## 此处依据“法无禁止即可为” 将未提及的结果都标记为CAN
                format_results.append(Attitude.NOMENTIONED)
        return format_results         
            
           
        
    
    def saveresult(self,output_file_path):
        """
        将结果保存到JSON文件中
        """
        
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.results, json_file, ensure_ascii=False, indent=4)
        print(f"查询结果已保存到 {output_file_path}")
        