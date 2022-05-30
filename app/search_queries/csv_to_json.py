import os
import unicodedata
import string
import json
import csv

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.printable).lower()

curr_dir = os.path.dirname(os.path.abspath(__file__))
csv_target = os.path.join(curr_dir, "fr-en-dict.csv")
print(csv_target)

with open(csv_target,'r', encoding='utf8') as csv_file:
    content = csv.reader(csv_file, delimiter=';')
    print(content)
    fr_en_dict = {}
    for row in content:
        if remove_accents(row[0]) not in fr_en_dict:
            fr_en_dict[remove_accents(row[0])] = [row[3]]
        else:
            fr_en_dict[remove_accents(row[0])].append(row[3])
    with open(os.path.join(curr_dir,"fr-en-dict.json"),"w", encoding='utf8') as jsonfile:
        fr_en_json = json.dump(fr_en_dict, jsonfile ,ensure_ascii=False)
    