import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def scatterplot():
    pass




def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    country = 'India'
    cur.execute("SELECT 'GDP Info'.'GDP', Day1.day FROM 'GDP Info' JOIN Day1 ON 'GDP Info'.Country = Day1.day WHERE Day1.country = ?", (country, ))

if __name__ == "__main__":
    main()