import os
import subprocess

# 内置参数设置
projects_folder = '../pypi_source'  # 修改为实际的项目文件夹路径
output_directory = '../scan_results'       # 修改为实际的输出文件夹路径
failed_projects_file = os.path.join(output_directory, 'failed_projects.txt')  # 记录失败项目的文件

# 创建输出目录
os.makedirs(output_directory, exist_ok=True)

# 初始化失败项目列表
failed_projects = []

# 扫描每个项目并保存结果
for project_name in os.listdir(projects_folder):
    project_path = os.path.join(projects_folder, project_name)
    if os.path.isdir(project_path):
        tree_output = os.path.join(output_directory, f'{project_name}_tree.json')
        conflict_output = os.path.join(output_directory, f'{project_name}_conflict.json')
        c_r_path = os.path.join(output_directory, f'{project_name}_c_r.json')
        print(f"Scanning project: {project_name}")
        
        # 调用已有扫描脚本
        result = subprocess.run([
            'python', 'src/main.py',
            '--directory', project_path,
            '--output_tree', tree_output,
            '--output_conflict', conflict_output,
            "--output_c_r" , c_r_path
        ])
        
        # 检查返回码
        if result.returncode != 0:
            print(f"Failed to scan project: {project_name}")
            failed_projects.append(project_name)
        else:
            print(f"Results for {project_name} saved to {output_directory}")

# 将失败的项目记录到文件
if failed_projects:
    with open(failed_projects_file, 'w') as f:
        for project in failed_projects:
            f.write(f"{project}\n")
    print(f"Failed projects recorded in {failed_projects_file}")
else:
    print("All projects scanned successfully.")
