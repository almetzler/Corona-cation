import sqlite3
import json
import os

'''
1) grab some functions from past assignments
    readDataFromFile        HW8
    setUpDatabase           HW8
2) Set up some tables:
    based on setupcategories table from hw8...maybe
3a) accept input for starting value
    index into dectionary.keys list to make sure we don't get duplicates
        insert if UNIQUE?
    write to database
3b) read in data if file doesn't exist
    write first 20 points to database
    write the rest to a file
    read in that file the next time
3c) read in data
    order it by keys/list index
    check length of table
    index at length of table to length +20
'''
def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    if '.json' in filename:
        file_data = f.read()
        f.close()
        json_data = json.loads(file_data)
    elif '.csv' in filename:
        file_data = f.readlines()
        f.close()
        json_data={}
        for line in file_data:
            json_data[line.split(',')[0]]=line.split(',')[1]
    return json_data

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpTables(cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Days ('country' TEXT PRIMARY KEY, 'day' INTEGER, 'cases' INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Day1 ('country' TEXT PRIMARY KEY, 'day' INTEGER)")

'''    this wont work for this table
def fillDaysTable(file,cur,conn):    
    cur.execute(f"SELECT COUNT (*) FROM Days") # how many values do I currently have in my table
    startindx = cur.fetchone[0] #assigns count of rows to my starting index
    endindx = startindx + 20 #assigns my ending index to be 20 after my start
    data = readDataFromFile(file) #returns dictionary of country:data
    guide = data.keys() # gives me an easy way to index into my dictionary
    for i in range(startindx,endindx):
        country = guide[i] #dictionry of country: [(day, case) tuples]
        days = data[country] #list of (day, cases) tuples
        for day in days: #these are tuples (day,cases)
            cur.execute("INSERT INTO Days (country, day, cases) VALUES (?,?)",(country,day[0],day[1]))
'''        

def fillDay1Table(file,cur,conn):    
    cur.execute(f"SELECT COUNT (*) FROM Day1") # how many values do I currently have in my table
    startindx = cur.fetchone()[0] #assigns count of rows to my starting index
    endindx = startindx + 20 #assigns my ending index to be 20 after my start
    print(f'{startindx},{endindx}')
    data = readDataFromFile(file) #returns dictionary of country:data
    guide = list(data.keys()) # gives me an easy way to index into my dictionary
    for i in range(startindx,endindx):
        country = guide[i] #dictionry of country: case 100
        day = data[country] #case 100
        cur.execute("INSERT INTO Day1 (country, day) VALUES (?,?)",(country,day))
    conn.commit()

def main():
    cur, conn = setUpDatabase('coronacation.db')
    setUpTables(cur,conn)
    fillDay1Table('daysto100.csv',cur,conn)

if __name__ == "__main__":
    main()