import os
import subprocess

class VirtualEnvManager:
    def __init__(self, python_version, env_name="venv", env_path="."):
        self.python_version = python_version
        self.env_name = env_name
        self.env_path = os.path.join(env_path, env_name)
        self.create_virtualenv()

    def create_virtualenv(self):
        if os.path.exists(self.env_path):
            print(f"虚拟环境已存在: {self.env_path}")
            return

        print(f"正在创建虚拟环境: {self.env_path} 使用 {self.python_version}...")
        try:
            subprocess.run(
                [self.python_version, "-m", "virtualenv", self.env_path],
                check=True
            )
            print(f"虚拟环境已创建: {self.env_path}")
        except subprocess.CalledProcessError as e:
            print(f"创建虚拟环境时发生错误: {e}")
            raise

    def run_in_virtualenv(self, command):
        """
        在虚拟环境中运行指定命令。
        
        参数:
            command (list): 要运行的命令，例如 ["python", "-m", "pip", "install", "requests"]。
        """
        if os.name == "nt":  # Windows 系统
            activate_script = os.path.join(self.env_path, "Scripts", "activate.bat")
        else:  # Unix 系统
            activate_script = os.path.join(self.env_path, "bin", "activate")

        # 拼接命令，在激活虚拟环境后执行
        full_command = f"source {activate_script} && {' '.join(command)}" if os.name != "nt" else f"{activate_script} && {' '.join(command)}"
        print(f"执行命令: {full_command}")
        subprocess.run(full_command, shell=True, check=True)

# 示例
env_manager = VirtualEnvManager(python_version="python3.8", env_name="myenv", env_path=".")
env_manager.run_in_virtualenv(["python", "--version"])
