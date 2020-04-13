from bs4 import BeautifulSoup
import requests
import re

def get_info_from_table():
    base_url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class' : 'wikitable'}).find_all('tr')
    country_list = []
    gdp_info = {}
    for row in table[393:]:
        cells = row.find_all('td')
        country = cells[1].text.strip()
        if '[' in country:
            country = re.findall(r'(\w+)\[\w+\s\d+\]', country)
            country = country[0]
        gdp = cells[2].text.strip()
        gdp_info[country] = gdp
    print(gdp_info)

            
            

    
    '''
    for item in table[1168:]:
        country_list.append(item)'''

    print(country_list)
        # if item.text.strip() == 'World[25]':
        #     print(count)
        #     print(item.text)
    '''
    country_gdp_info = {}
    for row in all_rows[1:]:
        row_cells = row.find_all('td')
        country = row_cells[1].text.strip()
        gdp = row_cells[2].text.strip()
        country_gdp_info[country] = gdp
    print(table)'''

def main():
    print(get_info_from_table())

if __name__ == "__main__":
    main()