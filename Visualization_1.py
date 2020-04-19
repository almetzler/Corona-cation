import numpy as np
import matplotlib.pyplot as plt
import os
import json
import sqlite3
'''
1) Get list of tuples
2) Plot points
'''

# get values
def get_tups(country):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    cur.execute("SELECT cases FROM Days WHERE country=?",(country,))
    data_string = cur.fetchone()[0]
    data_list = data_string.split('\n')
    tup_list = [x.strip('()').split(',') for x in data_list]
    x_vals = [float(x[0]) for x in tup_list]
    y_vals = [float(x[1]) for x in tup_list]
    return x_vals, y_vals

def plot_progessions(country,topvalue=None):
    try:
        x,y=get_tups(country)
        plt.plot(x,y)
        plt.xlabel('days since case 1')
        plt.ylabel('cases confirmed')
        plt.title(f'CORONA-CATION ({country})')
        plt.xscale('linear')
        plt.yscale('linear')
        if topvalue:
            plt.ylim(-1*topvalue/500,topvalue)
        plt.show()
    except:
        print("error, something went wrong")
    
def plot_progessions_list(country_list,topvalue=None):
    try:
        title=''
        for country in country_list:
            x,y=get_tups(country)
            plt.plot(x,y)
            title=title+country+', '
        plt.legend(country_list,loc='upper left')
        plt.xlabel('days since case 1')
        plt.ylabel('cases confirmed')
        plt.title(f'CORONA-CATION ({title[:-2]})')
        if topvalue:
            plt.ylim(-1*topvalue/500,topvalue)
        plt.show()
    except:
        print('error, something went wrong')
    

def main():
    #plot_progessions("Norway")
    plot_progessions_list(["Turkey","Norway",'Germany']) 
    



if __name__ == "__main__":
    main()