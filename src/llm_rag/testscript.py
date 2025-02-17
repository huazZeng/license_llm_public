from QueryProcessor import QueryProcessor
from RAGProcessor import RAGProcessor
local_text_path = "license_llm\Data\data\data\licenses\BSD-2-Clause"
with open(local_text_path, 'r', encoding='utf-8') as file:
    text = file.read()
## RAG部分都调整在RAGProcessor中   
ragProcessor = RAGProcessor(text)


query_contents = ragProcessor.process_multiple_queries()


    
    # 执行查询
results = queryProcessor.process_all_queries(query_contents,ragProcessor.query_texts_default)



# queryProcessor.saveresult(output_file_path)
print(results)