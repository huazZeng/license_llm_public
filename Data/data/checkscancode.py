import json

with open('Data\data\\result.json', 'r') as file:
    data = json.load(file)
count=0
correctcount=0
for file in data['files']:
    if file['detected_license_expression_spdx']:
        if 'licenses/'+file['detected_license_expression_spdx'] == file['path'] :
            correctcount+=1
        else :
            print(f"{file['path']} != licenses/{file['detected_license_expression_spdx']}")
        count += 1    
print(f"Correct: {correctcount}/{count} ({correctcount/count*100:.2f}%)")