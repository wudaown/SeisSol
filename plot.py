#!/usr/bin/env python3
# _*_ coding:utf8 _*_

import matplotlib.pyplot as plt
import datetime
import numpy as np
from subprocess import Popen, check_output
import argparse
import time

yr = [300,1600]

# parser = argparse.ArgumentParser()
# parser.add_argument('i', help='IP of PDU', type=str)
# parser.add_argument('l', help='IP of PDU', type=str)
# args = parser.parse_args()
# ip = args.i
# ip2 = args.l

count = 0
aa = []
bb = []
# cc = []
# dd = []
while True:
    f = open('pdu.txt','a+')
    plt.yticks(np.arange(min(yr), max(yr)+1, 100))
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    count += 1
    time.sleep(2)
    ip = '140.221.235.132'
    #ip2 = '140.221.235.132'
    a = check_output(['snmpget','-v1','-c','public', '-O', 'vuq',ip, '.1.3.6.1.4.1.21239.5.2.3.1.1.9.1' ])
    a = int(a.decode().replace('\n', ''))
    t = str(datetime.datetime.time(datetime.datetime.now())).split('.')[0]
    # b = check_output(['snmpget','-v1','-c','public', '-O', 'vuq',ip2, '.1.3.6.1.4.1.21239.5.2.3.1.1.9.1' ])
    # b = int(b.decode().replace('\n', ''))
    aa.append(t)
    bb.append(a)
    # cc.append(b)
    f.write('From ' + ip+ ' at '+ t+' '+str(a)+'\n')
    # f.write('From ' + ip2+ ' at '+ t+' '+str(b)+'\n')
    f.close()
    if aa.__len__() == 60:
        aa = aa[1:]
        bb = bb[1:]
        # cc = cc[1:]
        plt.clf()
    plt.plot(aa, bb, '-o', color='orange')
    # plt.plot(aa, cc, '-o', color='blue')
    plt.axhline(y=1500, color='r', linestyle='-')
    plt.ylim(bottom=300)
    plt.pause(0.05)
    plt.draw()
