import sqlite3
import json
import os
import re
import csv
import requests

'''
Things to do:
1) grab some functions from APIStuff
    get_country_names
    country_days
    days_to_100
2) grab some functions from DBStuff
    fill Day1Table - but change it a little
3) functions to write
    something to check if a country is already in the table

''' 
def get_country_names():
    country_list = []
    resp = requests.get('https://api.covid19api.com/countries')
    data = json.loads(resp.text)
    
    for country in data:
        country_list.append(country['Country'])
    
    return country_list

def country_days(country):
    count=0
    day_tups = []
    url = f'https://api.covid19api.com/dayone/country/{country}/status/confirmed'
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data == {"message":"Not Found"}:
        print(f'data not found for {country}')
        return None
    start = True
    for day in data:
        if start:
            date = day['Date']
            total=0
            start=False

        newdate = day['Date']

        if newdate == date:
            total += int(day['Cases'])

        else:
            day_tups.append((count,total))
            total = int(day['Cases'])
            count+=1

        date=newdate
    return day_tups

def days_to_100(country):
    count=0
    tups = country_days(country)
    if tups == None:
        return None
    for day in tups:
        if day[1] >100:
            return count
        count+=1
    return None

def check_in_db(country,table,cur,conn):
    cur.execute(f"SELECT * FROM {table} WHERE country=?",(country,))
    if cur.fetchone() == None:
        return False
    else:
        return True

def fill_Day1_table(cur,conn):
    print('filling table')    
    cur.execute("SELECT COUNT (*) FROM Day1") # how many values do I currently have in my table
    num = cur.fetchone()[0]
    print(num)
    count=0
    c_list = get_country_names()
    for c in c_list:
        if count>=20:
            break
        if check_in_db(c,'Day1',cur,conn):
            print(f'{c} already in database')
            continue
        elif days_to_100(c)==None:
            print(f'{c} is not at 100 yet')
            continue
        else:
            cur.execute("INSERT INTO Day1 (country, day) VALUES (?,?)",(c,days_to_100(c)))
            print(f'writing data for {c}')
            count+=1
    conn.commit()

def fill_Days_table(cur,conn):
    print('filling table')    
    cur.execute("SELECT COUNT (*) FROM Days") # how many values do I currently have in my table
    num = cur.fetchone()[0]
    print(num)
    count=0
    c_list = get_country_names()
    for c in c_list:
        if count>=20:
            break
        if check_in_db(c,'Days',cur,conn):
            print(f'{c} already in database')
            continue
        elif country_days(c) == None:
            print(f'no data found for {c}')
            continue
        else:
            slist = [str(x) for x in country_days(c)]
            string='\n'.join(slist)
            if len(string) == 0:
                print(f'no data found for {c}')
                continue
            cur.execute("INSERT INTO Days (country, '(day,cases)' ) VALUES (?,?)",(c,string))
            print(f'writing data for {c}')
            count+=1
    conn.commit()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Days ('country' TEXT PRIMARY KEY, '(day,cases)' TEXT)")
    #cur.execute("CREATE TABLE IF NOT EXISTS Day1 ('country' TEXT PRIMARY KEY, 'day' INTEGER)")
    #fill_Day1_table(cur,conn)
    fill_Days_table(cur,conn)
    #cur.execute("DROP TABLE IF EXISTS Days")
    #cur.execute("DROP TABLE IF EXISTS Day1")
    print('done')

if __name__ == "__main__":
    main()