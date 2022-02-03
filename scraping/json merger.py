import glob
import json
from os import read

read_files = glob.glob("C:/Users/Brendan/Desktop/teacher jsons/*")
bigList = []

for file in read_files:
    f = open(file)
    data = json.load(f)
    bigList.extend(data)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(bigList, f, ensure_ascii=False, indent=4)