from abc import ABC, abstractmethod
import subprocess
import re
import os
import requests
from .dependencyTool import dependencyTool
class PyDependencyTool(dependencyTool):
    def __init__(self,use_pipreqs=True):
        self.patterns = {
            'python': re.compile(r'^\s*(?:from\s+(\S+)\s+import|import\s+(\S+))'),
            'javascript': re.compile(r'^\s*(?:require\(\s*["\'](\S+)["\']\s*\)|import\s+(\S+))'),
            'java': re.compile(r'^\s*import\s+(\S+);'),
            'cpp': re.compile(r'^\s*#\s*include\s+<(\S+)>')
        }
        self.use_pipreqs = use_pipreqs  # Default method for extracting dependencies

    def initial(self, file_path: str):
        """Initialize the scanner with the given file path."""
        self.file_path = file_path

    def extract_dependencies_py(self, file_path):
        """Extract Python dependencies using pipreqsnb."""
        file_extension = os.path.splitext(file_path)[1]
        language = self.detect_language(file_extension)
        if language == "python":
            result = subprocess.run(['pipreqsnb', '--print', file_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            dependencies = re.findall(r'^\s*([\w\-]+)==([\d\.]+)\s*$', output, re.MULTILINE)
            formatted_dependencies = [f"{name}" for name, _ in dependencies]
        else :
            formatted_dependencies= [ ]
        return formatted_dependencies

    def extract_dependencies_manual(self, file_path):
        """Extract dependencies manually by scanning the file."""
        dependencies = []
        file_extension = os.path.splitext(file_path)[1]
        language = self.detect_language(file_extension)
        if language and language in self.patterns:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    match = self.patterns[language].match(line)
                    if match:
                        dependency = match.group(1) or match.group(2)
                        if dependency and dependency.split('.')[0] not in dependencies:
                            dependencies.append(dependency.split('.')[0])
        return dependencies

    def extract_dependencies(self, file_path):
        """Switch between pipreqsnb and manual extraction methods."""
        if self.use_pipreqs:
            return self.extract_dependencies_py(file_path)
        else:
            return self.extract_dependencies_manual(file_path)

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

    def scan_directory(self, directory):
        """Recursively scan a directory for dependencies."""
        all_dependencies = {}
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                dependencies = self.extract_dependencies(file_path)
                if dependencies:
                    all_dependencies[file_path] = dependencies
        return all_dependencies

    def get_license(self, package_name: str) -> str:
        """Fetch the license of a Python package from PyPI."""
        url = f'https://pypi.org/pypi/{package_name}/json'
        response = requests.get(url)
        response_json = response.json()
        if 'message' not in response_json:
            license = response_json['info'].get('license', None)
        else:
            license = 'NONE'
        return license
