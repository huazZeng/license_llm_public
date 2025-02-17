import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
from config import license_terms




# 定义一个虚拟文档类
class VirtualDocument:
    def __init__(self, content, metadata):
        self.page_content = content
        self.metadata = metadata


# 定义余弦相似度计算
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def extract_complete_sentence(text, part):
        sentences = re.split(r'(?<=[。！？；.?!;])\s*', text)
        for sentence in sentences:
            if part in sentence:
                return sentence
        return ""

class RAGProcessor:
    def __init__(self, text,model_name="sentence-transformers/sentence-t5-large"):
        self.embedding = HuggingFaceEmbeddings(model_name=model_name)
        self.query_texts_default = [term[1] for term in license_terms.values()]
        self.license_terms = license_terms
        
        self.process(text)
        self.text=text
    def clean_document(self, text):
        """
        清理许可证文本内容
        """
        text = re.sub(r'".+?"(?:\s+\S+){0,5}\s+means?:?\s+.*?[.?!;]', '', text)
        text = re.sub(r'“.+?”(?:\s+\S+){0,5}\s+means?:?\s+.*?[.?!;]', '', text)
        text = re.sub(r'".+?"(?:\s+\S+){0,5}\s+refers?:?\s+to+.*?[.?!;]', '', text)
        text = re.sub(r'“.+?”(?:\s+\S+){0,5}\s+refers?:?\s+to+.*?[.?!;]', '', text)
        text = re.sub(r'Copyright \(C\)[^.?!;]*[.?!;]', '', text)
        text = re.sub(r'http[s]?://\S+', '', text)
        text = re.sub(r'\n\s*\n', '\n', text).strip()

        return text
    
    def split_and_embed(self, text= None, chunk_size=100, chunk_overlap=50):
        """
        分块并生成嵌入向量
        """
        if text is None:
            text = self.text
        
        # 将清理后的文本封装为虚拟文档
        virtual_document = VirtualDocument(text, metadata={"source": "input_text"})

        # 分块
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents([virtual_document])

        print(f"Number of document chunks: {len(docs)}")

        # 嵌入文档内容
        doc_embeddings = [self.embedding.embed_query(doc.page_content) for doc in docs] if len(docs) > 50 else []
        self.docs = docs 
        self.doc_embeddings = doc_embeddings
        return docs, doc_embeddings

    def process(self, text, chunk_size=100, chunk_overlap=50):
        """
        对输入的许可证字符串进行清理、分块和嵌入处理
        """
        cleaned_text = self.clean_document(text)
        return self.split_and_embed(cleaned_text, chunk_size, chunk_overlap)

    def process_query(self, query_text):
        """
        输出结果为query ，可以从这里
        """
        # 获取查询的向量表示
        
        output_content = (
        f"Listed below are the main parts of a license. Please tell me its attitude towards '{query_text}' with 'can', 'must', 'cannot' "
        "or 'nomentioned', together with relevant original sentences in the license and your reasons for inference. (If the license "
        f"explicitly permits '{query_text}', give me 'can'; if it explicitly bans '{query_text}' please give me 'cannot'; if it explicitly asks "
        f"for '{query_text}', please give me 'must'. If it hasn't explicitly mentioned '{query_text}', please give me 'nomentioned'.):\n\n"
        )
        if len(self.docs) <= 50:
            output_content += self.text
        else:
            query_embedding = self.embedding.embed_query(query_text)
            # 计算查询和文档的余弦相似度
            similarities = [
                (cosine_similarity(query_embedding, self.doc_embedding), self.docs[j].page_content)
                for j, self.doc_embedding in enumerate(self.doc_embeddings)
            ]
            
            # 按照相似度降序排列
            similarities.sort(key=lambda x: x[0], reverse=True)
            
            # 选择前n个相似度最高的文档块
            n = min(max(5, int(0.05 * len(self.docs))), 15)
            found_sentences = set()
            output_content = ""
            
            for score, chunk in similarities[:n]:
                result_parts = re.split(r'(?<=[。！？；.?!;])\s*', chunk)
                for part in result_parts:
                    if part.strip():
                        complete_sentence = extract_complete_sentence(self.text, part)
                        if complete_sentence and complete_sentence not in found_sentences:
                            found_sentences.add(complete_sentence)
                            output_content += f"Relevant Sentence: {complete_sentence}\n"
            
        return output_content
    
    def process_multiple_queries(self, query_texts=None):
        """
        批量处理多个查询
        """
        if query_texts is None:
            query_texts = self.query_texts_default
        output_contents = []
        for query_text in query_texts:
            output_content = self.process_query(query_text)
            output_contents.append(output_content)
        return output_contents