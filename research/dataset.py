import os
import subprocess
import tarfile

def download_source(package_name, output_dir="pypi_source"):
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(["pip", "download", "--no-binary", ":all:", "--no-deps", package_name, "-d", output_dir])
    
    for file in os.listdir(output_dir):
        if file.endswith(".tar.gz"):
            with tarfile.open(os.path.join(output_dir, file), "r:gz") as tar:
                tar.extractall(output_dir)
            print(f"Extracted: {file}")
            os.remove(os.path.join(output_dir, file))

with open('library_selected.txt', mode='r', newline='', encoding='utf-8') as f:
    data = f.readlines()
    for line in data:
        download_source(line.strip())
