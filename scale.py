#!/usr/bin/env python3
# _*_ coding:utf8 _*_

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import os
import random
import argparse

plt.style.use('seaborn-white')

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIXGeneral']
plt.rcParams['font.weight'] = 'light'


params = {'legend.fontsize': 16}
plt.rcParams.update(params)

os.chdir('./scale')
FILELIST=os.listdir('.')
HARD_FILE=[x for x in FILELIST if 'non' in x]
HARD_FILE.sort()

print(HARD_FILE)

number_of_colors = HARD_FILE.__len__()

color = ['#4AC29C', '#E768B6']

def gflop_graph(input_filelist, color):
    x = [10,20,30,40]
    y = [ i for i in range(7,18)]
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
        if j == 0:
            c = color[0]
        else:
            c = color[1]
        if label_input[1][0] == 'G':
            markerfacecolor = 'none'
        else:
            markerfacecolor = c
        plt.plot(x,wp, marker='o', markerfacecolor=markerfacecolor,
                markersize=8, color=c, label=label, linewidth=2)
        plt.plot(x,tt, marker='o', markerfacecolor=markerfacecolor,
                markersize=8, color=c, linestyle='dashed', linewidth=2)
    plt.xticks(x, x)
    plt.yticks(y, y)
    plt.tick_params(axis='both', labelsize=16)
    plt.xlabel('Number of cores', fontsize=20, labelpad=3)
    plt.ylabel('GFLOPS per core', fontsize=20, labelpad=3) 
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.2), ncol=4)
    plt.box(on=None)
    for i in range(7, 18):
        plt.axhline(y=i, linestyle='--', color='black', alpha=0.05)
    
    plt.show()


def et_graph(input_filelist, color):
    x = [10,20,30,40]
    y = [ i for i in range(0,110,10)]
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
        if label_input[1][0] == 'G':
            markerfacecolor = 'none'
        else:
            markerfacecolor = c
        plt.plot(x,et, marker='o', markerfacecolor=markerfacecolor,
                markersize=8, color=c, label=label, linewidth=2)
    plt.xticks(x, x)
    plt.yticks(y,y)
    plt.tick_params(axis='both', labelsize=16)
    plt.xlabel('Number of cores', fontsize=20, labelpad=3)
    plt.ylabel('Extrapolated time (h)', fontsize=20, labelpad=3) 
    plt.legend(loc=9, bbox_to_anchor=(0.5,-0.2), ncol=4)
    plt.box(on=None)
    for i in range(0, 110, 10):
        plt.axhline(y=i, linestyle='--', color='black', alpha=0.05)
    plt.show()

    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("g",type=str,help="Type of graph [GFLOPS per core, Extrapolated Time]", choices=['gflop', 'et'])
    args = parser.parse_args()
    if args.g == 'et':
        et_graph(HARD_FILE, color)
    else:
        gflop_graph(HARD_FILE, color)
