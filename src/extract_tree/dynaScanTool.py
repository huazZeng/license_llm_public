
import os
import subprocess
from .dependencyTool import dependencyTool
import re
licensemapping = {
    "Apache 2" : "Apache-2.0",
    "" : "NONE",
    
}
def extract_license_info(text):
        """
        提取 License: 到 Location: 之间的内容，并移除最后的换行符。
        
        参数:
            text (str): 包含 License 和 Location 信息的字符串。
        
        返回:
            str: 提取到的 License 信息。
        """
        # 正则表达式匹配 License 到 Location 之间的内容
        match = re.search(r"License:\s*(.*?)\nLocation:", text, re.DOTALL)
        if match:
            # 返回去掉最后一个换行符的结果
            return match.group(1).rstrip("\n")
        return "NONE"

class dynaScanTool(dependencyTool):
    def __init__(self, python_version="3.11.2", env_name="venv", env_path="."):
        """
        使用 virtualenv 构建虚拟环境。

        参数:
            python_version (str): 指定 Python 版本，例如 "python3.8"。
            env_name (str): 虚拟环境的名称，默认为 "venv"。
            env_path (str): 虚拟环境的存储路径，默认为当前路径。
        """
        self.python_version = python_version
        self.env_name = env_name
        self.env_path = os.path.join(env_path, env_name)
        

    def initial(self, file_path: str):
        """
        初始化扫描工具并创建虚拟环境。

        参数:
            file_path (str): 文件路径。
        """
        self.file_path = file_path
        print(f"初始化文件路径: {file_path}")
        self.create_virtualenv()
        self.RequirementInstall(file_path)

    def create_virtualenv(self):
        """
        创建虚拟环境。
        """
        # 检查路径是否已存在
        if os.path.exists(self.env_path):
            print(f"虚拟环境已存在: {self.env_path}")
            return

        print(f"正在创建虚拟环境: {self.env_path} 使用 {self.python_version}...")
        try:
            result = subprocess.run(
                ["virtualenv", "-p", self.python_version, self.env_path],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"虚拟环境已创建: {self.env_path}")
        except subprocess.CalledProcessError as e:
            print(f"创建虚拟环境时发生错误: {e}")
            raise
        except FileNotFoundError:
            print(f"未找到指定的 Python 版本: {self.python_version}")
            raise

    def extract_dependencies(self, file_path: str):
        """
        提取文件的依赖模块。

        参数:
            file_path (str): 文件路径。

        返回:
            list: 检测到的模块列表。
        """
        dependencies = []
        file_extension = os.path.splitext(file_path)[1]
        language = self.detect_language(file_extension)
        if language == 'python':
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # 正则表达式匹配 import 语句
            import_pattern = re.compile(r"^\s*(?:import|from)\s+([\w\.]+)", re.MULTILINE)
            imports = import_pattern.findall(code)
            top_level_modules = {imp.split('.')[0] if '.' in imp else imp for imp in imports}
            modules = set(top_level_modules)
            modules = list(modules)
            for module in modules:
                try:
                    if module :
                        __import__(module)
                except ImportError as e:
                    modules.remove(module)
                # 去重保留唯一的模块名
            
        else:
            modules = []
        return list(modules)

    def get_license(self, package_name: str) -> str:
        """
        获取指定包的许可证信息。

        参数:
            package_name (str): 包名。

        返回:
            str: 许可证信息。
        """
        # print(f"尝试获取包 {package_name} 的许可证信息...")
        try:
            result = subprocess.run(
                ["pip", "show", package_name],
                check=True,
                capture_output=True,
                text=True
            )
            output = result.stdout
            license = extract_license_info(output)
            
            
                
            
            if 'AND' in license:
                license = license.split('AND')
                license = license[0].strip()
            elif 'OR' in license:
                license = license.split('OR')
                license = license[0].strip()
            elif 'WITH' in license:
                license = license.split('WITH')
                license = license[0].strip()  
            
            if license in licensemapping:
                license = licensemapping[license]
            return license
           
        except subprocess.CalledProcessError:
            return "NONE"
    
    def RequirementInstall(self, path: str):
        """
        使用 pipreq 获取项目依赖并安装。

        参数:
            path (str): 项目路径。
        """
        # 确保路径存在
        if not os.path.exists(path):
            raise FileNotFoundError(f"路径 {path} 不存在。")

        # 检查是否已存在 requirements.txt
        requirements_path = os.path.join(path, "requirements.txt")
        if os.path.exists(requirements_path):
            print(f"requirements.txt 已存在，跳过生成。")
        else:
            # 使用 pipreq 生成 requirements.txt
            print("正在生成 requirements.txt 文件...")
            try:
                subprocess.run(["pipreqs", path, "--force"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"运行 pipreq 时发生错误: {e}")
                return

        # 使用 pip 安装依赖
        print("正在安装依赖...")
        try:
            subprocess.run(["pip", "install", "-r", requirements_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"安装依赖时发生错误: {e}")
            return

        print("依赖安装完成。")

    
    def detect_language(self, file_extension):
        """Detect programming language based on file extension."""
        if file_extension in ['.py']:
            return 'python'
        elif file_extension in ['.js']:
            return 'javascript'
        elif file_extension in ['.java']:
            return 'java'
        elif file_extension in ['.cpp', '.h']:
            return 'cpp'
        return None
    
    
if __name__ == "__main__":
    extractor = PyDependencyTool()
    