#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import csv
dowjones = pd.read_csv('dowjones.csv')
dowjones = list(dowjones['Close'])
result = list()
result.append(['TYPE', 'cash_old', 'cash_new', 'trade', 'asset_old', 'asset_new', 'price_old', 'price_new'])
price_old = -1
cash = 1000  # our money
asset = 0  # our dowjones papers

for price_new in dowjones:
    if price_old > price_new:  # buy if price decreased
        buy = cash / price_new
        TYPE = 'BUY'
        if buy == 0:
            TYPE = 'None'

        result.append([TYPE, cash, 0, buy, asset, asset + buy / price_new, price_old, price_new])
        asset = asset + cash / price_new
        cash = 0

    elif price_old < price_new:  # sell if price increased
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

with open('tit_for_tat_reversed.csv', 'w') as datafile:
    writer = csv.writer(datafile)
    writer.writerows(result)
