from abc import ABC, abstractmethod
import json
import subprocess
import os

class scancodetool(ABC):
    
    

    def run_command_call(self,command):
        try:
            env = os.environ.copy()
            env["PATH"] += os.getcwd()+ '\\src\\scancode-toolkit\\scancode' 

           
            result = os.system(command)
            if result == 0:
                print(f"Command succeeded: {' '.join(command)}")
            else:
                print(f"Command failed: {' '.join(command)} with return code {return_code}")
        except Exception as e:
            print(f"Exception while running command: {e}")

        
        
    ## TODO 可以将scancode设置为环境变量
    def initial(self, file_path: str) :
        self.filename2license={}
        self.filename2matchtext = {}
        output_file = "./scanresult.json"
        scan_options = '-l' # Default scan options
        command = 'src\\scancode-toolkit\\scancode ' + scan_options +  ' --license-text'+' --json-pp ' + output_file +' '+ file_path
        print(f"Scanning files in {file_path}...")
        output = self.run_command_call(command)
       
            
        with open(output_file) as f:
            
            data=json.load(f)
            filedetails= data['files']
            dictionary= data['headers'][0]['options']['input'][0]
            dictionary = os.path.dirname(dictionary)
            for fileitem in filedetails:
                path = dictionary+'/'+ fileitem['path']

                if fileitem['license_detections']:
                    
                    
                    
                    self.filename2license[path]=fileitem["detected_license_expression_spdx"]
                    matched_text = ""
                    for context in fileitem['license_detections'][0]["matches"]:
                        matched_text += context['matched_text']
                    self.filename2matchtext[path]=matched_text
                    
                else :
                    self.filename2license[path]='NONE'
                    self.filename2matchtext[path]='NONE'
                    
        return 
   
    def scan_file_license(self, file_path: str) -> str:
        if file_path not in self.filename2license:
            return 'NONE'
        return self.licensefilter(self.filename2license[file_path])

   
    def scan_file_generateGoodSentense(self, file_path: str) ->str :
        return None
        
    
    def append_goodsentence_onTree(self, file_path: str) ->str :
        if file_path not in self.filename2matchtext:
            return 'NONE'
        return self.filename2matchtext[file_path]
    
    def licensefilter(self,license):
        Nonefilterlist = ["LicenseRef-scancode-unknown-license-reference","LicenseRef-scancode-public-domain","LicenseRef-scancode-free-unknown"]
        unknownfilterlist = ['LicenseRef-scancode-generic-cla']
        if license in Nonefilterlist:
            return "NONE"
        elif license in unknownfilterlist:
            return "UNKNOWN"
        else:
            if 'AND' in license:
                license = license.split('AND')
                return license[0].strip()
            elif 'OR' in license:
                license = license.split('OR')
                return license[0].strip()
            elif 'WITH' in license:
                license = license.split('WITH')
                return license[0].strip()
            return license 