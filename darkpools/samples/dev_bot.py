import tradersbot as tt
import math
import random
import pandas as pd
import time

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

#global variables
tick = 0
tickers = ['USDCAD','USDJPY','EURUSD','USDCHF','CHFJPY','EURJPY','EURCHF','EURCAD']
marketTickers = ['USDCAD', 'EURUSD', 'USDCHF', 'USDJPY']
darkTickers = ['CHFJPY','EURJPY','EURCHF','EURCAD']
state = {}
darkpools = {}

orderbook = {}
#cash = {'USD': 100000, 'JPY': 0, 'EUR': 0, 'CHF': 0, 'CAD': 0}
triangs = {'USDCAD': ['EURUSD', 'EURCAD'], 'USDCHF':['EURUSD', 'EURCHF'], 'USDJPY': ['EURUSD', 'EURJPY']}

#, 'USDCHF': ['USDJPY', 'CHFJPY']

t_last_ord = 0
time_last_clear = 0
time_last_update = 0

old_pnl = 0
pnl = 0


arb_threshold = 0.007
trans_fee = 0.0001


fileTrade = open("onTrade.txt", 'w')
#fileonTrader = open("onTrader.txt", 'w')
#file = open("test.txt", 'w')
for i in tickers:
    state[i] = {}

for i in darkTickers:
    darkpools[i] = -1
#file = open("testfile.txt","w")
"""
EURJPY
USDCHF
EURCHF
EURCAD
"""


def f(msg, order):
    global tick
    msg = msg["market_state"]
    idx = msg["ticker"]
    state[idx]["bids"] = msg['bids']
    state[idx]["asks"]  = msg['asks']
    #print(tick)
    arbitrage(idx, order)
    tick+=1


def arbitrage(idx, order):
    global state, triangs, arb_threshold, darkpools

    try:
        idx_reg = triangs[idx][0]
        idx_dark = triangs[idx][1]

        p1a = min(state[idx]['asks'].keys())
        p1b = max(state[idx]['bids'].keys())

        p2a = min(state[idx_reg]['asks'].keys())
        p2b = max(state[idx_reg]['bids'].keys())

        quantity = min(1000, min(state[idx]['asks'][p1a], state[idx_reg]['asks'][p2a]))

        p1 = round((float(p1a)+float(p1b))/2.02,2)
        p2 = round((float(p2a)+float(p2b))/2.02,2)
        if(darkpools[idx_dark]==-1):
            p3 = p1*p2-arb_threshold
            quantity = 10
        else:
            p3 = (darkpools[idx_dark] + p1*p2-arb_threshold)/2
        #print(p1, p2, p3)


    #print(quantity)
    #p = abs(float(state['USDCAD']['asks'][0])-float(state['USDCAD']['asks'][0])) + float(state['USDCAD']['asks'][0])

        order.addTrade(idx, True, quantity, p1, None)

        order.addTrade(idx_reg, True, quantity, p2, None)

        order.addTrade(idx_dark, True, -quantity, p3, None)

        """order.addSell('USDCHF', quantity = 200, price = p1)
        order.addBuy('EURUSD', quantity = 200, price = p2)
        order.addBuy('EURCHF', quantity = 200, price = p2/p1 - arb_threshold)
        """
        #print('Traded')
        #print(state)
        """quantity = 500
        idx = 'USDCAD'
        side = get_side()
        if side == 'buy':
            order.addBuy(idx, quantity=quantity, price=0.99)
        else:
            order.addSell(idx, quantity=quantity, price=1.01)
            """
    except:
        pass


def g(msg,order):
    global tick, old_pnl, pnl
    old_pnl = pnl
    pnl =  str(msg['trader_state']['default_pnl'])
    print("profit: " + pnl)

    if(tick%100 > 5 and tick%100<12):
        c = 0
        for ob in msg['trader_state']['open_orders']:
            print(ob)
            if(c==3):
                break
            order.addCancel(msg['trader_state']['open_orders'][ob]['ticker'], (msg['trader_state']['open_orders'][ob]['order_id']))
            c+=1

    #fileonTrader.write("tick: " + str(tick)+ " \n {}".format(str(msg) + "\n"))
    tick+=1

def k(msg, order):
    global tick, darkpools
    #print(msg)
    for ob in msg['trades']:
        if ob['ticker'] in darkTickers:
            darkpools[ob['ticker']] = float(ob['price'])
    fileTrade.write("tick: " + str(tick)+ " \n {}".format(str(msg) + "\n"))
    tick+=1
"""def arbit(msg, order):
    global tick
"""
t.onMarketUpdate = f
t.onTraderUpdate = g
t.onTrade = k
t.run()
