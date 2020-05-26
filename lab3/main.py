#!/usr/bin/python
# -*- coding: utf-8 -*-
# lab 3

import csv
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import pdfkit
import pylab
from matplotlib import mlab
import re
import collections


def tarificate(income_cost=1, outcome_cost=3, sms_cost=1, data_file_path='./data.csv'):

    array = []
    call = 0
    in_call = 0
    sms = 0

    with open('data.csv' , newline='') as File:
        reader = csv.reader(File)

        for row in reader:
            array.append(row)


    for i in range(1,10):
        if '915642913' in array[i][1]:
            call+=float(array[i][3])
            sms+=float(array[i][4])
        if '915642913' in array[i][2]:
            in_call+=float(array[i][3])

    call_value = (call+in_call)*1
    if sms in range(5,10): sms_value = 5*0 + (sms-5)*1
    elif sms > 10: sms_value = 5*0 + 5*1 + (sms-10)*2
    else: sms_cost = 0

    return call_value, sms_value


def get_ms(time):
    timepattern = r"[:.]"
    splited = re.split(timepattern, time)
    return int(splited[0]) * 60 * 60 * 1000 + int(splited[1]) * 60 * 1000 + int(splited[2]) * 1000 + int(splited[3])


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


def create_pdf(output, bik, src_num, inn, kpp, dst, number, date, customer, tel, sms, net):
    template_file = open('./schet.html.j2', 'r')
    template = template_file.read()
    template_file.close()
    env = Environment(loader=FileSystemLoader('.'))
    schet = env.get_template('schet.html.j2')
    sum = tel + sms + net
    schet_content = schet.render(BIK=bik, SRC_NUM=src_num,INN=inn,KPP=kpp,DST_NUM=dst,NUMBER=number,DATE=date,CUSTOMER=customer,TEL=tel,SMS=sms,NET=net,SUM=sum)
    schet_html = open('tmp_html.html', 'w')
    schet_html.write(schet_content)
    schet_html.close()
    pdfkit.from_url('./tmp_html.html', output)


counter = tarificate()

tel, sms = tarificate()
net = internet('192.168.250.59')

create_pdf(
    './schet.pdf',
    '80808080',
    '121212121212',
    '999999999',
    '1010101010',
    '17171717171717171',
    '1',
    '11.08.1998',
    u'Дружинина Д. Б.',
    tel,
    sms,
    round(net, 2)
)
