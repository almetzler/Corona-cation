import sqlite3
import requests
import json
import os
from fuzzywuzzy import fuzz
'''
full_path = os.path.join(os.path.dirname(__file__), 'daysto50.csv')
f = open(full_path)
file_data = f.readlines()
f.close()

data={}
for line in file_data:
    data[line.split(',')[0]]=line.split(',')[1]
    
print(data['India'])

for x in 'banananananan':
    while y<5:
        print(x)
        y+=1
        break

while y<5:
    for x in '123456789':
        print(x)
        y+=1
        break

y=0
for x in '123456789':
    print(x)
    y+=1
    if y>=5:
        break

c_list=[(1,2),(3,4),(5,6),7,8,9]
slist=[str(x) for x in c_list]

for c in c_list:
    if c>=7:
        break
    if c<3:
        continue
    elif c%2 == 0:
        continue
    else:
        print(c)

print(','.join(slist))


print(fuzz.partial_ratio("Taiwan", "Taiwan, Republic of China"))
print('done')
'''
def cdict():
    resp = requests.get('https://api.covid19api.com/countries')
    data = json.loads(resp.text)
    return data
print(cdict()[0])