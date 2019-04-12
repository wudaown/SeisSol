#!/usr/bin/env python3
# _*_ coding:utf8 _*_

import matplotlib.pyplot as plt
import os
import random
import argparse

plt.rcParams['figure.dpi']= 300
plt.style.use('seaborn-white')

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12


os.chdir('./scale')
FILELIST=os.listdir('.')
#HARD_FILE=[x for x in FILELIST if 'hard' in x]
HARD_FILE=[x for x in FILELIST if 'non' in x]
HARD_FILE.sort()

print(HARD_FILE)

number_of_colors = HARD_FILE.__len__()

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
#color = ['#4286f4', '#41f46b', '#d941f4', '#f44141']
color = ['#4AC29C', '#E768B6']

def gflop_graph(input_filelist, color):
    x = [10,20,30,40]
    for j in range(HARD_FILE.__len__()):
        y_file = open(HARD_FILE[j], 'r')
        label_input = (HARD_FILE[j].split('_'))
        label_input[0] = label_input[0].upper()
        if '1' in label_input[1]:
            label_input[1] = 'G' + label_input[2][-1]
        else:
            label_input[1] = 'L' + label_input[2][-1]
        label_input = label_input[0:2]
        label = ' '.join(label_input)
        wp = []
        tt = []
        for i in y_file:
            if 'WP' in i:
                wp.append(float(i.replace('\n','').split(' ')[-1]))
            if 'TOTAL' in i:
                tt.append(float(i.replace('\n','').split(' ')[-1]))
        #if j == 0 or j == 1:
        #    c = color[0]
        # elif j == 2 or j == 4:
        #     c = color[1]
        # elif j == 3 or j == 5:
        #     c = color[2]
        if j == 0:
            c = color[0]
        else:
            c = color[1]
        if label_input[1][0] == 'G':
            markerfacecolor = 'none'
        else:
            markerfacecolor = c
        plt.plot(x,wp, marker='o', markerfacecolor=markerfacecolor, markersize=12, color=c, label=label)
        plt.plot(x,tt, marker='o', markerfacecolor=markerfacecolor, markersize=12, color=c, linestyle='dashed')
    plt.xticks(x, x)
    plt.xlabel('Number of cores')
    plt.ylabel('GFLOPS per core') 
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=4)
    
    plt.show()


def et_graph(input_filelist, color):
    x = [10,20,30,40]
    for j in range(HARD_FILE.__len__()):
        print(HARD_FILE[j])
        y_file = open(HARD_FILE[j], 'r')
        label_input = (HARD_FILE[j].split('_'))
        label_input[0] = label_input[0].upper()
        if '1' in label_input[1]:
            label_input[1] = 'G' + label_input[2][-1]
        else:
            label_input[1] = 'L' + label_input[2][-1]
        label_input = label_input[0:2]
        label = ' '.join(label_input)
        et = []
        for i in y_file:
            if 'hour' in i:
                et.append(float(i.replace('\n','').split(' ')[-1]))
        print(et)
        if j == 0:
            c = color[0]
        else:
            c = color[1]
        # if j == 0 or j == 1:
        #     c = color[0]
        # elif j == 2 or j == 4:
        #     c = color[1]
        # elif j == 3 or j == 5:
        #     c = color[2]
        if label_input[1][0] == 'G':
            markerfacecolor = 'none'
        else:
            markerfacecolor = c
        plt.plot(x,et, marker='o', markerfacecolor=markerfacecolor, markersize=12, color=c, label=label)
    plt.xticks(x, x)
    plt.xlabel('Number of cores')
    plt.ylabel('Extrapolated Time ( Hours )') 
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=4)
    
    
    plt.show()

    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("g",type=str,help="Type of graph [GFLOPS per core, Extrapolated Time]", choices=['gflop', 'et'])
    args = parser.parse_args()
    if args.g == 'et':
        et_graph(HARD_FILE, color)
    else:
        gflop_graph(HARD_FILE, color)
