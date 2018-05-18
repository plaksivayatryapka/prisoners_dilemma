#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import csv
dowjones = pd.read_csv('dowjones.csv')
dowjones = list(dowjones['Close'])
result = list()
result.append(['TYPE', 'cash_old', 'cash_new', 'trade', 'asset_old', 'asset_new', 'price_old_2', 'price_old', 'price_new'])

price_old = -1
price_old_2 = -1
cash = 1000  # our money
asset = 0  # our dowjones papers
for price_new in dowjones:
    if price_old_2 == -1:  # pass first iteration
        result.append(['None', cash, cash, 0, asset, asset, price_old_2, price_old, price_new])
        price_old_2 = price_new
        continue

    if price_old == -1:  # pass second iteration
        result.append(['None', cash, cash, 0, asset, asset, price_old_2, price_old, price_new])
        price_old = price_new
        continue

    if price_old_2 > price_old > price_new and cash:  # buy if price decreased for 2 days in row
        buy = cash

        result.append(['BUY', cash, cash - buy, buy, asset, asset + buy / price_new, price_old_2, price_old, price_new])
        asset = asset + buy / price_new
        cash = cash - buy

    elif price_old_2 < price_old < price_new and asset:  # sell if price increased for 2 days in row
        sell = asset * price_new

        result.append(['SELL', cash, cash + sell, sell, asset, asset - sell / price_new, price_old_2, price_old, price_new])
        asset = asset - sell / price_new
        cash = cash + sell

    else:
        result.append(['None', cash, cash, 0, asset, asset, price_old_2, price_old, price_new])

    price_old_2 = price_old
    price_old = price_new

sell = asset * price_new  # sell final assets
cash = cash + sell
result.append(['sell', cash, cash + sell, sell, asset, asset - sell / price_new, price_old, price_new])
print 'efficiency = ', cash / 1000.0

with open('result_days_reversed.csv', 'w') as datafile:
    writer = csv.writer(datafile)
    writer.writerows(result)
