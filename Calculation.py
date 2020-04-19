import sqlite3
import os
import numpy as np

def calculate_average_days(cur, conn):
    cur.execute("SELECT day FROM Day1")
    country_list = cur.fetchall()
    count = 0

    for country in country_list:
        count += country[0]

    average = count / len(country_list)

    full_path = os.path.join(os.path.dirname(__file__), 'averagedays.txt')
    fle = open(full_path,'w')
    fle.write(f'The average number of days to get to 100 cases is {average}.')
    fle.close()


def calculate_correlation(cur, conn):
    cur.execute("SELECT country FROM Day1")
    country_list1 = cur.fetchall()
    gdp_day_list = []
    for country in country_list1:
        try:
            cur.execute("SELECT 'GDP Info'.'GDP', Day1.day FROM 'GDP Info' JOIN Day1 ON 'GDP Info'.Country = Day1.country WHERE Day1.country = ?", (country[0],))
            gdp_day = cur.fetchone()
            gdp_day_list.append(gdp_day)
        except:
            continue
    x_vals = []
    y_vals = []
    for item in gdp_day_list:
        if item != None:
            x_vals.append(item[1])
            y_vals.append(item[0])

    math = np.corrcoef(x_vals, y_vals)
    print(math)

    full_path = os.path.join(os.path.dirname(__file__), 'correlation.txt')
    fle = open(full_path,'w')
    fle.write(f'The correlation between days to 100 cases and GDP is {math[0][1]}.')
    fle.close()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    calculate_average_days(cur, conn)
    calculate_correlation(cur, conn)


if __name__ == "__main__":
    main()