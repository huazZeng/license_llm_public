from abc import ABC, abstractmethod

class dependencyTool(ABC):
    
    @abstractmethod
    def initial(self, file_path: str) :
        
        pass
    @abstractmethod
    def extract_dependencies(self, file_path: str):
        """
        扫描文件的许可证信息。

        参数:
            file_path (str): 文件的路径。

        返回:
            str: 许可证信息。
        """
        pass

    @abstractmethod
    def get_license(self, package_name: str) -> str:
        """
        获取 PyPI 上指定包的许可证信息。
        """
        pass
    
    
