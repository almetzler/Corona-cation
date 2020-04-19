import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def scatterplot(cur, conn):
    cur.execute("SELECT country FROM Day1")
    country_list = cur.fetchall()
    gdp_day_list = []
    for country in country_list:
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

    plt.plot(x_vals,y_vals,'b.')
    plt.xlabel('Days From 1 Case to 100')
    plt.ylabel('GDP')
    plt.title('Correlation Between Days to 100 Cases and GDP')
    plt.ylim(0, 500000)
    plt.show()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    scatterplot(cur, conn)

if __name__ == "__main__":
    main()