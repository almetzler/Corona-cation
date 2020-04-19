import sqlite3
import json
import os

full_path = os.path.join(os.path.dirname(__file__), 'daysto50.csv')
f = open(full_path)
file_data = f.readlines()
f.close()

data={}
for line in file_data:
    data[line.split(',')[0]]=line.split(',')[1]
    
print(data['India'])
'''
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
'''