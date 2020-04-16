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

def plot_progessions(country):
    x,y=get_tups(country)
    plt.plot(x,y)
    plt.xlabel('days since case 1')
    plt.ylabel('cases confirmed')
    plt.title(f'CORONA-CATION ({country})')
    

def main():
    plot_progessions("India")
    plot_progessions("Germany")
    plt.show()



if __name__ == "__main__":
    main()