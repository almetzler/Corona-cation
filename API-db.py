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

def fill_IDs(cur,conn):
    '''
    Inputs: none
    Outputs: a list of all of the country names that are listed on the API
    The purpose of this function is to provide an iterable so that when later
    going through the data we can make sure that we have gotten to all of the countries.
    '''
    country_list = []
    resp = requests.get('https://api.covid19api.com/countries')
    data = json.loads(resp.text)
    indx=1
    for country in data:
        c=country['Country']
        s=country['Slug']
        cur.execute("INSERT OR IGNORE INTO IDs (id, country, slug) VALUES (?,?,?)",(indx,c,s))
        #print((indx,c))
        indx+=1
    conn.commit()
'''
def country_days(country):
    
    Inputs: a country name
    Outputs: a list of (days since case 1, confirmed cases) tuples or None
    The purpose of this function is to return a list of tuples for a given
    country that can later be used to find the number of days to 100 cases
    and can be written to one of our tables, if no data has been reported
    for the country the function returns None.
    
    count=0
    day_tups = []
    url = f'https://api.covid19api.com/dayone/country/{country}/status/confirmed'
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data == {"message":"Not Found"}:
        #print(f'data not found for {country}')
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
'''
def fill_Days_table(cur,conn):
    cur.execute("SELECT * FROM IDs")
    countries = cur.fetchall()
    for row in countries:
        count=0
        c_id = row[0]
        cur.execute("SELECT * FROM Days WHERE id = ?",(c_id,))
        if cur.fetchone()!=None:
            #print(f'{row[1]} already written')
            continue
        #print(row)
        try:
            url = f'https://api.covid19api.com/dayone/country/{row[2]}/status/confirmed'
            resp = requests.get(url)
            data = json.loads(resp.text)
            if data == {"message":"Not Found"}:
                #print(f'data not found for {row[1]}')
                cur.execute("INSERT OR IGNORE INTO Days (id,day,cases) VALUES (?,?,?)", (c_id,None,None))
                continue
            if len(data) == 0:
                #print(f'data not found for {row[1]}')
                cur.execute("INSERT OR IGNORE INTO Days (id,day,cases) VALUES (?,?,?)", (c_id,None,None))
                continue
            start = True
            for day in data:
                if start:
                    date = day['Date']
                    total=0
                    start=False
                newdate = day['Date']
                #print(total)
                if newdate == date:
                    total += int(day['Cases'])
                else:
                    cur.execute("INSERT OR IGNORE INTO Days (id,day,cases) VALUES (?,?,?)", (c_id,count,total))
                    #print((c_id,count,total))
                    total = int(day['Cases'])
                    count+=1
                date=newdate
        except:
            print(f'data not found for {row[1]}')
            cur.execute("INSERT OR IGNORE INTO Days (id,day,cases) VALUES (?,?,?)", (c_id,None,None))
        conn.commit()
    print('done filling Days')
    


'''
def days_to_100(country):
    
    Inputs: a country name
    Outputs: either None or an integer
    The purpose of this function is to take a tuple list returned by country_days() 
    and return the day on which the number of confirmed cases rose above 100. If the 
    cases have yet to breach 100, the function returns None.
    
    count=0
    tups = country_days(country)
    if tups == None:
        return None
    for day in tups:
        if day[1] >100:
            return count
        count+=1
    return None
'''
'''
def check_in_db(c_id,table,cur,conn):
    
    Inputs: a country name, a table, a cursor, and a connection
    Outputs: a boolean value
    The purpose of this function is to determine whether data for
    a given country has already been entered into a given table.
    This can later be used to prevent duplicate values being entered
    into a table.
    
    cur.execute(f"SELECT * FROM {table} WHERE id=?",(c_id,))
    if cur.fetchone() == None:
        return False
    else:
        return True
'''
def fill_Day1_table(cur,conn):
    ''' 
    Inputs: a cursor and a connection
    Outputs: None
    The purpose of this function is to populate the table containing
    the days to 100 days. It only sends 20 data points at a time and
    ensures that no duplicate data points are entered by only adding
    a value to the table if check_in_db returns False.
    '''
    print('filling table')    
    cur.execute("SELECT COUNT (*) FROM Day1") # how many values do I currently have in my table
    num = cur.fetchone()[0]
    count=0
    cur.execute("SELECT * FROM IDs")
    c_list = cur.fetchall()
    for row in c_list:
        if count>=num+20:
            break
        c_id = row[0]
        cur.execute("SELECT MIN(day) FROM Days WHERE id=? AND cases>?",(c_id,100))
        day = cur.fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO Day1 (id, day) VALUES (?,?)",(c_id,day))
        #print(f'writing data for {c}')
        count+=1
        conn.commit()
    print(f'there are currently {num} rows in Day1.')
'''
def fill_Days_table(cur,conn):
    
    Inputs: a cursor and a connection
    Outputs: None
    The purpose of this function is to populate the table containing
    the day-by-day data. It only sends 20 data points at a time and ensures
    that no duplicate data points are entered by only adding a value to the
    table if check_in_db returns False
    
    print('filling table')    
    cur.execute("SELECT COUNT (*) FROM Days") # how many values do I currently have in my table
    num = cur.fetchone()[0]
    print(num)
    count=0
    c_list = get_country_names(cur,conn)
    for c in c_list:
        if count>=20:
            break
        if check_in_db(c,'Days',cur,conn):
            #print(f'{c} already in database')
            continue
        elif country_days(c) == None:
            #print(f'no data found for {c}')
            continue
        else:
            slist = [str(x) for x in country_days(c)]
            string='\n'.join(slist)
            if len(string) == 0:
                #print(f'no data found for {c}')
                continue
            cur.execute("INSERT INTO Days (country, cases ) VALUES (?,?)",(c,string))
            #print(f'writing data for {c}')
            count+=1
    conn.commit()
'''
def main():
    '''
    Inputs: None
    Outputs: None
    The purpose of this function is to specify which functions within the
    file should be called and the order in which they should be called. This
    is where one would specify the inputs for each of the functions they
    would like to use. We use this function to create the tables within our
    database which we later populate using other functions. This is also where
    we specify the database cursor and connection to be used in the other functions.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS IDs ('id' INTEGER PRIMARY KEY, 'country' TEXT, 'slug' TEXT,UNIQUE (id,country,slug))")
    cur.execute("CREATE TABLE IF NOT EXISTS Days ('id' INTEGER, day INTEGER, cases INTEGER,UNIQUE(id,day,cases))")
    cur.execute("CREATE TABLE IF NOT EXISTS Day1 ('id' INTEGER PRIMARY KEY, 'day' INTEGER,UNIQUE(id,day))")
    
    fill_IDs(cur,conn)
    fill_Day1_table(cur,conn)
    fill_Days_table(cur,conn)

    #cur.execute("DROP TABLE IF EXISTS Days")
    #cur.execute("DROP TABLE IF EXISTS IDs")
    #cur.execute("DROP TABLE IF EXISTS Day1")
    print('done')

if __name__ == "__main__":
    main()