#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import csv
dowjones = pd.read_csv('dowjones.csv')
dowjones = list(dowjones['Close'])
result = list()
result.append(['TYPE', 'cash_old', 'cash_new', 'trade', 'asset_old', 'asset_new', 'price_old', 'price_new'])

cash = 1000  # our money
asset = 0  # our dowjones papers
price_old = -1
for price_new in dowjones:
    if price_old == -1:  # pass first iteration
        price_old = price_new
        continue

    if price_old < price_new:  # buy if price increased
        buy = cash * (1 - price_old / price_new)
        result.append(['buy', cash, cash - buy, buy, asset, asset + buy / price_new, price_old, price_new])
        asset = asset + buy / price_new
        cash = cash - buy

    elif price_old > price_new:  # sell if price decreased
        sell = cash * (1 - price_new / price_old)
        if asset * price_new > sell:
            result.append(['sell', cash, cash + sell, sell, asset, asset - sell / price_new, price_old, price_new])
            asset = asset - sell / price_new
            cash = cash + sell

        elif asset * price_new < sell and asset != 0:  # if not enough money
            sell = asset * price_new
            result.append(['sell', cash, cash + sell, sell, asset, asset - sell / price_new, price_old, price_new])
            asset = asset - sell / price_new
            cash = cash + sell

    price_old = price_new

sell = asset * price_new  # sell final assets
result.append(['sell', cash, cash + sell, sell, asset, asset - sell / price_new, price_old, price_new])

with open('result.csv', 'w') as datafile:
    writer = csv.writer(datafile)
    writer.writerows(result)
