from bs4 import BeautifulSoup
import requests
import re
import os
import json

def get_info_from_table():
    base_url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class' : 'wikitable'}).find_all('tr')
    gdp_info = {}
    for row in table[393:]:
        cells = row.find_all('td')
        country = cells[1].text.strip()
        if '[' in country:
            country = re.findall(r'(\w+)\[\w+\s\d+\]', country)
            country = country[0]
        gdp = cells[2].text.strip().replace(',', '')
        gdp_info[country] = int(gdp)
    return gdp_info

def write_json(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    fle = open(full_path,'w')
    fle.write(json.dumps(get_info_from_table()))         

def main():
    get_info_from_table()
    write_json('country_gdp_info.json')

if __name__ == "__main__":
    main()