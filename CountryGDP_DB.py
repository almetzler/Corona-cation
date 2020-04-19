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


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'GDP Info' ('Country'  TEXT PRIMARY KEY, 'GDP' INTEGER, UNIQUE ('Country', 'GDP'))")
    GDP_dict = get_info_from_table(cur, conn)
    fill_table(cur, conn, GDP_dict)


if __name__ == "__main__":
    main()