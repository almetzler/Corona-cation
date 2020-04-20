from bs4 import BeautifulSoup
import requests
import re
import os
import json
import sqlite3

def get_info_from_table(cur, conn):
    base_url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class' : 'wikitable'}).find_all('tr')
    gdp_info = {}
    cur.execute(f"SELECT COUNT (*) FROM 'GDP Info'")
    startindex = cur.fetchone()[0]
    for row in table[392 + startindex: 392 + startindex + 20]:
        cells = row.find_all('td')
        country = cells[1].text.strip()
        if '[' in country:
            country = re.findall(r'(\w+)\[\w+\s\d+\]', country)
            country = country[0]
        gdp = cells[2].text.strip().replace(',', '')
        gdp_info[country] = int(gdp)
    return gdp_info

# Inputs: cursor and connection 
# Output: A dictionary named gdp_info that has the countries as the key and their GDP as the value
# The purpose of the function get_info_from_table() is to create an iterable in order to go through while making tables in our database



def fill_table(cur, conn, country_dict):
    cur.execute(f"SELECT COUNT (*) FROM 'GDP Info'")
    num_rows = cur.fetchone()[0]
    print(num_rows)
    count = 0
    for country in country_dict:
        if count >= 20:
            break
        else:
            cur.execute("INSERT OR IGNORE INTO 'GDP Info' (Country, GDP) VALUES (?, ?)", (country, country_dict[country]))
            count += 1
    conn.commit()

# Inputs: cursor, connection, dictionary with a country as key and GDP as the value
# Output: None
# The purpose of fill_table() is to create and populate a table in our database with each row containing a country and its GDP. The dictionary we take as input is the output of get_info_from_table()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'GDP Info' ('Country'  TEXT PRIMARY KEY, 'GDP' INTEGER, UNIQUE ('Country', 'GDP'))")
    GDP_dict = get_info_from_table(cur, conn)
    fill_table(cur, conn, GDP_dict)

# Input: None
# Output: None
# The purpose of the main() function is to run the other functions in the file in a specified order. Additionally, this function specifies the database to populate and creates a table if it does not already exist in the database. It also establishes a cursor and a connection.


if __name__ == "__main__":
    main()