from bs4 import BeautifulSoup
import requests
import re

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

            

def main():
    print(get_info_from_table())

if __name__ == "__main__":
    main()