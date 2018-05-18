#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import csv
from random import randint
dowjones = pd.read_csv('dowjones.csv')
dowjones = list(dowjones['Close'])
result = list()
result.append(['TYPE', 'cash_old', 'cash_new', 'trade', 'asset_old', 'asset_new', 'price_old', 'price_new'])

cash = 1000  # our money
asset = 0  # our dowjones papers
price_old = -1
for price_new in dowjones:
    random = randint(0, 1)

    if random == 1:  # buy if 1
        buy = cash / price_new
        TYPE = 'BUY'
        if buy == 0:
            TYPE = 'None'

        result.append([TYPE, cash, 0, buy, asset, asset + buy / price_new, price_old, price_new])
        asset = asset + cash / price_new
        cash = 0

    else:  # sell if 0
        sell = asset * price_new
        TYPE = 'SELL'
        if sell == 0:
            TYPE = 'None'

        result.append([TYPE, cash, cash + sell, sell, asset, 0, price_old, price_new])
        asset = 0
        cash = cash + sell

    price_old = price_new

sell = asset * price_new  # sell final assets
cash = cash + sell
result.append(['sell', cash, cash + sell, sell, asset, asset - sell / price_new, price_old, price_new])
print 'efficiency = ', cash / 1000.0

with open('random.csv', 'w') as datafile:
    writer = csv.writer(datafile)
    writer.writerows(result)
