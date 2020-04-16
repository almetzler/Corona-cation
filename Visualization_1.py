import numpy as np
import matplotlib.pyplot as plt
import os
import json
'''
1) Get list of tuples
2) Plot points
'''

# get values
def get_tups(country):
    full_path = os.path.join(os.path.dirname(__file__), 'countrydata.json')
    x_vals=[]
    y_vals=[]
    with open(full_path) as fle:
        data = fle.read()
        countrydic = json.loads(data)
    for line in countrydic[country]:
        x_vals.append(line[0])
        y_vals.append(line[1])
    return x_vals, y_vals

def plot_progessions(country,topvalue=None):
    try:
        x,y=get_tups(country)
        plt.plot(x,y)
        plt.xlabel('days since case 1')
        plt.ylabel('cases confirmed')
        plt.title(f'CORONA-CATION ({country})')
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
        plt.legend(country_list)
        plt.xlabel('days since case 1')
        plt.ylabel('cases confirmed')
        plt.title(f'CORONA-CATION ({title[:-2]})')
        if topvalue:
            plt.ylim(-1*topvalue/500,topvalue)
        plt.show()
    except:
        print('error, something went wrong')
    

def main():
    #plot_progessions("India") produces wanted figure
    #plot_progessions("Gerany") gives error
    #plot_progessions_list(["India","Germany",'United States of America'],5000) produces correct figure
    #plot_progessions_list(["India","Germay",'United States of America'],5000) gives error
    



if __name__ == "__main__":
    main()