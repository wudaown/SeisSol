#!/usr/bin/env python3
# _*_ coding:utf8 _*_

import matplotlib.pyplot as plt
import os


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'STIXGeneral'
#plt.rcParams['font.monospace'] = 'Times New Roman'
plt.rc('axes.spines', **{'bottom':False, 'left':False, 'right':False, 'top':False})
os.chdir('./config')
filelist = os.listdir('.')
print(filelist)
GFLOP_HARD_FILE=[x for x in filelist if 'hard' in x]
GFLOP_HARD_FILE.sort()
TTS_FILE=[x for x in filelist if 'tts' in x]
TTS_FILE.sort()


def get_data(input_file,normalize=None):
    data = []
    file = open(input_file, 'r')
    for i in file:
        try:
            data.append(float(i.replace('\n', '')))
        except ValueError as e:
            pass
    if normalize:
        data = [normalize[i] / data[i] for i in range(len(data))]

    return data

def extract_data(input_filelist, normalize=False):
    array_name = []
    d = {}
    for i in input_filelist:
        array_name.append(i.split('_', 1)[1].upper())
    
    if normalize:
        d[array_name[0]] = get_data(input_filelist[0])
        for i in range(1, len(array_name)):
            d[array_name[i]] = get_data(input_filelist[i], d[array_name[0]])
    else:
        for i in range(len(array_name)):
            d[array_name[i]] = get_data(input_filelist[i])

    if normalize:
        d[array_name[0]] = [1] * d[array_name[0]].__len__()

    data = []
    array_len = d[array_name[0]].__len__()
    for i in range(array_len):
        dd = {}
        for j in range(array_name.__len__()):
            dd[array_name[j]] = d[array_name[j]][i]
        name = 'order' + str(i+2)
        locals()[name] = dd
        data.append(eval(name))

    return data




tts_data = extract_data(TTS_FILE, normalize=True)
gflops_hard_data = extract_data(GFLOP_HARD_FILE)



fig, axs = plt.subplots(2,4, sharey='row')
def plot(data, ylabel, row, order=False):
    for i in range(len(data)):
        names = list(data[i].keys())
        values = list(data[i].values())
        if i == 0:
            axs[row][i].set_ylabel(ylabel, fontsize=12)
        axs[row][i].bar(names,values, color=['#76C8AE', '#EA96CA', '#EA96CA'])
        if order:
            axs[row][i].set_title('O'+str(i+4))
        for j in axs[row][i].patches:
    # get_x pulls left or right; get_height pushes up or down
            #x_pos = (j.get_x())
            #if x_pos < 0:
            #    x_pos = -0.2
            #else:
            #    x_pos = 0.8
            axs[row][i].text(j.get_x()+0.2, j.get_height()/1.3, \
            str(round((j.get_height()), 2)), fontsize=10, color='black',
                rotation=90)

plot(tts_data, 'Speedup', 1)
plot(gflops_hard_data, 'GFLOPS', 0, order=True)


fig.suptitle('SKX', weight=1)

plt.show()


