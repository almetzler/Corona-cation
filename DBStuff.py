import sqlite3
import json
import os

'''
1) grab some functions from past assignments
    readDataFromFile        HW8
    setUpDatabase           HW8
2) Set up some tables:
    based on setupcategories table from hw8...maybe
'''
def readJDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpDaysTable(data,cur,conn):
    cur.execute("CREATE TABLE Days (country, TEXT PRIMARY KEY, day, INTEGER, cases, INTEGER)")
    for country in data:
        pass

def main():
    json_data = readJDataFromFile('countrydata.json')
    cur, conn = setUpDatabase('coronacation.db')

if __name__ == "__main__":
    main()