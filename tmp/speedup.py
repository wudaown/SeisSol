#!/usr/bin/env python3
# _*_ coding:utf8 _*_

import matplotlib.pyplot as plt
import os

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

os.chdir('./config')
filelist = os.listdir('.')
GFLOP_HARD_FILE=[x for x in filelist if 'hard' in x]
GFLOP_HARD_FILE.sort()
GFLOP_NON_FILE=[x for x in filelist if 'non' in x]
GFLOP_NON_FILE.sort()
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
    print(array_name)
    
    if normalize:
        d[array_name[0]] = get_data(input_filelist[0])
        for i in range(1, len(array_name)):
            d[array_name[i]] = get_data(input_filelist[i], d[array_name[0]])
    else:
        for i in range(len(array_name)):
            d[array_name[i]] = get_data(input_filelist[i])

    if normalize:
        d[array_name[0]] = [1] * d[array_name[0]].__len__()
    print(d)

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
gflops_non_data = extract_data(GFLOP_NON_FILE)
gflops_hard_data = extract_data(GFLOP_HARD_FILE)


#def extract_data(sc_file, bl_file, bl_1_file, normalize=False):
#    file = open(bl_file, 'r')
#    bl_tts = []
#    for i in file:
#        try:
#            bl_tts.append(float(i.replace('\n', '')))
#        except ValueError as e:
#            pass
#    
#    # bl_tts = bl_tts[::2] even elements
#    #bl_tts = bl_tts[1::2]
#    #bl_tts = [float(x) for x in bl_tts]
#    
#    file = open(sc_file, 'r')
#    sc_tts = []
#    for i in file:
#        try:
#            sc_tts.append(float(i.replace('\n', '')))
#        except ValueError as e:
#            pass
#
#    file = open(bl_1_file, 'r')
#    bl16_tts = []
#    for i in file:
#        try:
#            bl16_tts.append(float(i.replace('\n', '')))
#        except ValueError as e:
#            pass
#    
#    #sc_tts = sc_tts[1::2]
#    if normalize:
#        sc_tts = [bl_tts[i] / sc_tts[i] for i in range(len(sc_tts))]
#        bl16_tts = [bl_tts[i] / bl16_tts[i] for i in range(len(sc_tts))]
#        bl_tts = [1] * bl_tts.__len__()
#    #sc_tts = [float(x) for x in sc_tts]
#    data = []
#    for i in range(len(sc_tts)):
#        d = {}
#        d['BL'] = bl_tts[i]
#        d['BL PREFETCH'] = bl16_tts[i]
#        d['SC'] = sc_tts[i]
#        name = 'order' + str(i+2)
#        locals()[name] = d
#        data.append(eval(name))
#    return data
#

#tts_data = extract_data(sc_file='tts_sc', bl_file='tts_bl',bl_1_file='tts_bl_1', normalize=True)
#gflops_non_data = extract_data(sc_file='non_sc', bl_file='non_bl', bl_1_file='non_bl_1')
#gflops_hard_data = extract_data(sc_file='hard_sc', bl_file='hard_bl', bl_1_file='hard_bl_1')
fig, axs = plt.subplots(3,4, figsize=(130000,90000) ,sharey='row', dpi=300)
def plot(data, ylabel, row):
    for i in range(len(data)):
        names = list(data[i].keys())
        values = list(data[i].values())
        if i == 0:
            axs[row][i].set_ylabel(ylabel, fontsize=14)
        axs[row][i].bar(names,values, color=['#76C8AE', '#98AAD0', '#EA96CA'])
        axs[row][i].set_title('O'+str(i+4))
        for j in axs[row][i].patches:
    # get_x pulls left or right; get_height pushes up or down
            #x_pos = (j.get_x())
            #if x_pos < 0:
            #    x_pos = -0.2
            #else:
            #    x_pos = 0.8
            axs[row][i].text(j.get_x(), j.get_height()/2, \
            str(round((j.get_height()), 2)), fontsize=8, color='white',
                rotation=0)

plot(tts_data, 'Speedup', 0)
plot(gflops_non_data, 'GFLOPS (NON ZERO)', 1)
plot(gflops_hard_data, 'GFLOPS (HARDWARE)', 2)

#for i in range(len(tts_data)):
#    names = list(tts_data[i].keys())
#    values = list(tts_data[i].values())
#    if i == 0:
#        axs[0][i].set_ylabel('Speedup', fontsize=18)
#    axs[0][i].bar(names,values)
#    axs[0][i].set_title('O'+str(i+2))
#
#for i in range(len(gflops_non_data)):
#    names = list(gflops_non_data[i].keys())
#    values = list(gflops_non_data[i].values())
#    if i == 0:
#        axs[1][i].set_ylabel('GFLOPS (non zero)', fontsize=18)
#    axs[1][i].bar(names,values)
#    axs[1][i].set_title('O'+str(i+2)+'\nHSW')


#for i, row in enumerate(axs):
#    for j, cell in enumerate(row):
#        cell.imshow(np.random.rand(32,32))
#        if i == len(axs) - 1:
#            cell.set_xlabel("X LABEL FOR EACH COLUMN".format(j + 1))
#        if j == 0:
#            cell.set_ylabel("Y LABEL FOR EACH ROW".format(i + 1))

fig.suptitle('HSW')

plt.show()


