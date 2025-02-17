from abc import ABC, abstractmethod

class ScanTool(ABC):
    
    @abstractmethod
    def initial(self, file_path: str) :
        
        pass
    @abstractmethod
    def scan_file_license(self, file_path: str) -> str:
        """
        扫描文件的许可证信息。

        参数:
            file_path (str): 文件的路径。

        返回:
            str: 许可证信息。
        """
        pass

    @abstractmethod
    def scan_file_generateGoodSentense(self, file_path: str) -> str:
        """
        扫描文件并生成适合的句子。

        参数:
            file_path (str): 文件的路径。

        返回:
            str: 生成的句子。
        """
        pass
    
    @abstractmethod
    def append_goodsentence_onTree(self, node):
        
        pass
    
    
