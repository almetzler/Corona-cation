import sqlite3
import os
import numpy as np

def calculate_average_days(cur, conn):
    cur.execute("SELECT * FROM Day1")
    country_list = cur.fetchall()
    count = 0

    for country in country_list:
        if country[1] != None: 
            count += country[1]

    average = count / len(country_list)

    full_path = os.path.join(os.path.dirname(__file__), 'averagedays.txt')
    fle = open(full_path,'w')
    fle.write(f'The average number of days to get to 100 cases is {average}.')
    fle.close()

# Input: cursor and connection
# Output: None
# The purpose of calculate_average_days() is to write a text file named averagedays.txt to your local computer. This text file gives the average number of days to get to 100 cases of COVID-19


def calculate_correlation(cur, conn):
    cur.execute("SELECT * FROM 'GDP Info'")
    country_list = cur.fetchall()
    gdp_day_list = []
    for country in country_list:
        try:
            cur.execute("SELECT 'GDP Info'.'GDP', Day1.day FROM 'GDP Info' JOIN Day1 ON 'GDP Info'.'Country ID' = Day1.id WHERE Day1.id = ?", (country[0],))
            gdp_day = cur.fetchone()
            gdp_day_list.append(gdp_day)
        except:
            continue

    x_vals = []
    y_vals = []
    val_list = [x for x in gdp_day_list[1:] if None not in x]
    for item in val_list:
        x_vals.append(item[1])
        y_vals.append(item[0])

    math = np.corrcoef(x_vals, y_vals)
    print(math)

    full_path = os.path.join(os.path.dirname(__file__), 'correlation.txt')
    fle = open(full_path,'w')
    fle.write(f'The correlation between days to 100 cases and GDP is {math[0][1]}.')
    fle.close()

# Input: cursor and connection
# Output: None
# The purpose of calculate_correlation() is to write a text file named correlation.txt to your local computer. This text file gives the correlation between the number of days to 100 cases and country GDP.


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    calculate_average_days(cur, conn)
    calculate_correlation(cur, conn)

# Input: None
# Output: None
# The purpose of the main() function is to run the other functions in the file in a specified order. Additionally, this function specifies the database to pull information from and establishes a connection and cursor. 


if __name__ == "__main__":
    main()