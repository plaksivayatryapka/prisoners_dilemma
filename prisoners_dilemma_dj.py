#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import mean
from statistics import median
import random
import numpy as np
import subprocess
import os
from pprint import pprint
import datetime

PATH = '/home/anon/coding/prisoners_dilemma/'
increase = 1
decrease = 1

dowjones = pd.read_csv(PATH + 'dowjones.csv')
dowjones = tuple(dowjones['Close'])
last = dowjones[0]


def tit_for_tat_complex(**kwargs):
    index = kwargs['index']
    lag = kwargs['lag']
    cash = float(kwargs['cash'])
    asset = float(kwargs['asset'])
    is_reversed = kwargs['is_reversed']

    last = index[0]
    actions_count = 0
    previouses = list()

    # FORM PREVIOUS VALUES BEFORE LAUNCHING LOOP
    if lag != 1:
        for current in index[1:lag]:
            if current > last:
                previouses.append(True)
            else:
                previouses.append(False)

            last = current

    # ITERATE OVER INDEX
    for current in index[(lag + 1):]:
        if not is_reversed:
            if current > last and cash and False not in previouses:
                asset = cash / current
                cash = 0.0
                actions_count += 1

            elif current < last and asset and True not in previouses:
                cash = asset * current
                asset = 0.0
                actions_count += 1

        elif is_reversed:
            if current > last and asset and False not in previouses:
                cash = asset * current
                asset = 0.0
                actions_count += 1

            elif current < last and cash and True not in previouses:
                asset = cash / current
                cash = 0.0
                actions_count += 1

        if lag != 1:
            del previouses[0]
            if current > last:
                previouses.append(True)
            else:
                previouses.append(False)

        last = current
    return {'cash': cash + asset * current, 'actions_count': actions_count}


for current in dowjones[1:]:
    if current > last:
        increase *= current / last
    else:
        decrease *= last / current

    last = current

print 'median strategy result = %s' % (increase/decrease) ** 0.5

results = list()
for i in range(1, 10, 1):
    result = tit_for_tat_complex(index=dowjones, lag=i, cash=1000, asset=0, is_reversed=False)
    result_reversed = tit_for_tat_complex(index=dowjones, lag=i, cash=1000, asset=0, is_reversed=True)
    results.append([i,
                    result['cash'],
                    result['actions_count'],
                    result_reversed['cash'],
                    result_reversed['actions_count']])

df = pd.DataFrame(results, columns=['threshold', 'tit_for_tat', 'actions_count', 'tit_for_tat_reversed', 'actions_count'])
df = df.set_index('threshold')
df.to_csv(PATH + 'results.csv')
