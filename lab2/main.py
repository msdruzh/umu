#!/usr/bin/python
# -*- coding: utf-8 -*-

import pylab
from matplotlib import mlab
import re
import collections


def get_ms(time):
    splited_time = re.split(r"[:.]", time)
    return int(splited_time[0]) * 60 * 60 * 1000 + int(splited_time[1]) * 60 * 1000 + int(splited_time[2]) * 1000 + int(splited_time[3])


def internet(target):
    free_mb = 1000.0 / 1024
    factor = 1

    xlist = []
    ylist = []
    data = dict()
    nf_file_path = './nf_decoded'

    nf_file = open(nf_file_path, 'r')
    cost = 0

    for line in nf_file.readlines():
        finish = len(line)
        i = 0
        while i < finish:
            if (line[i] == ' ' and line[i + 1] == ' '):
                line = line[:i] + line[i + 1:]
                finish -= 1
            else:
                i += 1
        linedata = line.split(' ')
        if (target in [linedata[6].split(':')[0], linedata[4].split(':')[0]]):
            data.update({get_ms(linedata[1]): (float(linedata[8]) / 1024 / 1024)})
            cost += factor * (float(linedata[8]) / 1024 / 1024)

    sorted_array = collections.OrderedDict(sorted(data.items()))
    for key, value in sorted_array.items():
        xlist.append(key)
        ylist.append(value)
    xlist.sort()
    pylab.plot(xlist, ylist)
    pylab.savefig('./graphic')

    if cost > 500:
        cost -= 250
    else:
        cost = cost / (factor / 0.5)
    return cost


print('Стоимость услуг интернет: ' + str(internet('192.168.250.59')))
