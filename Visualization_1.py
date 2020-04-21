import numpy as np
import matplotlib.pyplot as plt
import os
import json
import sqlite3
from fuzzywuzzy import fuzz
'''
1) Get list of tuples
2) Plot points
'''

# get values
def get_tups(country):
    '''
    Inputs: a country name
    Outputs: a list of x-values and a list of y-values
    The purpose of this function is to take data from our database
    from the day-by-day table and then split the tuples into a list
    of day values and a list of case values that can later be graphed
    as a visualization.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'coronacation.db')
    cur = conn.cursor()
    c_id = None
    cur.execute("SELECT * FROM IDs")
    for row in cur:
        c = row[1].split(',')
        if fuzz.partial_ratio(country, c[0]) >= 90:
            c_id = row[0]
    cur.execute("SELECT day,cases FROM Days WHERE id=?",(c_id,))
    day_tups = cur.fetchall()
    x_vals = [float(x[0]) for x in day_tups]
    y_vals = [float(x[1]) for x in day_tups]
    return x_vals, y_vals

def plot_progessions(country,topvalue=None,dayvalue=None):
    '''
    Inputs: a country name and an optional top value
    Outputs: a figure
    The purpose of this function is to plot the progression of the
    number of cases in a given country as time progresses. The optional
    top value parameter can be used to specify the highest value that
    you would like on the y-axis, this can be helpful as slow early
    growth is easily dwarfed by later rapid growth.
    '''
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
        if dayvalue:
            plt.xlim(0,dayvalue)
        plt.show()
    except:
        print("error, something went wrong")
    
def plot_progessions_list(country_list,topvalue=None,dayvalue=None):
    '''
    Inputs: a list of country names and an optional top value
    Outputs: a figure
    The purpose of this function is to plot the progression of the
    number of cases in several countries as time progresses. The
    optional top value parameter can be used to specify the highest
    value that you would like on the y-axis, this can be helpful as
    slow early growth is easily dwarfed by later rapid growth and
    extreme numbers for one country can dwarf the smaller numbers of
    another country.
    '''
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
        if dayvalue:
            plt.xlim(0,dayvalue)
        plt.show()
    except:
        print('error, something went wrong')
    

def main():
    '''
    Inputs: None
    Outputs: None
    The purpose of this function is to specify which functions within
    the file should be called and the order in which they should be
    called. This is where one would specify the inputs for each of the
    functions they would like to use.
    '''
    plot_progessions("United States of America")
    #plot_progessions_list(["Turkey","Norway",'Germany']) 
    



if __name__ == "__main__":
    main()