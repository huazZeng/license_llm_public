
import random

with open('library_license.txt', mode='r', newline='', encoding='utf-8') as f:
    data = f.readlines()
    result = []
    for line in data:
        result.append(line.split(' ::::: ')[0])
    print(result)

with open('library_selected.txt', mode='w', newline='', encoding='utf-8') as f:
    for line in result:
        I = random.random()
        if I >0.98:
            f.write(line + '\n')