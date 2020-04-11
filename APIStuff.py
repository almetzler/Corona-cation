'''
Game Plan:
1) Make a list of Countries
2) Get the date of their first case
3) Get Date of 50th case
4) find number of days between 1 and 50
5) put in all in a csv on github
    list of (country name , days from day 1 to day 50)
6) maybe also create a json file of day by day number of cases
    {country name:[(day,case),(day,case)...]}

Functions to make:
1) Count days 
    Turn date into quantifiable thing
    maybe just have an iterator that starts at day 1 stops when cases == 50
2) Fetch data from API
3) Write to database
4) Functions to grab from past projects/homeworks
    setUpDatabase       HW8
    main                kinda everywhere
    write_csv           Project 2

'''

# AND SO IT BEGINS
# Get some imports, never sure what you might need
import os
import requests
import json
import re
import csv

# Task 1: Get a list of country names
def get_country_names():
    country_list = []
    resp = requests.get('https://api.covid19api.com/countries')
    data = json.loads(resp.text)
    
    for country in data:
        country_list.append(country['Country'])
    
    return country_list


# Task 2: create dictionary of country:tuple list of (day,case) pairs
def get_days():
    country_dic={}
    lst = get_country_names()
    for country in lst:
        count=0
        day_tups = []
        url = f'https://api.covid19api.com/dayone/country/{country}/status/confirmed'
        resp = requests.get(url)
        data = json.loads(resp.text)
        if data == {"message":"Not Found"}:
            continue
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
            #some countries are also split into counties so I have to do something about that
            
        country_dic[country] = day_tups
    return country_dic

# Task 2.1 rewrite task 2 so that I can later call the function on a country and get the tuple list
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

# Task 3: Get days from 1 reported case to 50
def days_to_50(country):
    count=0
    tups = country_days(country)
    if tups == None:
        return None
    for day in tups:
        if day[1] >50:
            return count
        count+=1
    return None

# Task 3: Write a csv of (country name, days to 50)
def write_csv(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    fle = open(full_path,'w')
    fle.write('country,days to 50')
    data = get_country_names()
    for country in data:
        country = country.split(',')[0]
        if days_to_50(country) == None:
            continue
        fle.write(f'\n{country},{days_to_50(country)}')
    fle.close()

# Task 4: Dump json sting of dictionaty of day:tuples
def write_json(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    fle = open(full_path,'w')
    fle.write(json.dumps(get_days()))


def main():
    #print(get_country_names()[:5])
    #print(get_days()['India'])
    #print(country_days("United States of America"))
    #print(days_to_50('United states of america'))
    write_csv('daysto50.csv')
    write_json('countrydata.json')
    print('done')



if __name__ == "__main__":
    main()