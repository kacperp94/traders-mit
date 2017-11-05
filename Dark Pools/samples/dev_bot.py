import tradersbot as tt
import math
import random
import pandas as pd
import time

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')
tick = 0
tickers = ['USDCAD','USDJPY','EURUSD','USDCHF','CHFJPY','EURJPY','EURCHF','EURCAD']
marketTickers = ['USDCAD', 'EURUSD', 'USDCHF', 'USDJPY']
state = {}

case_meta = {}
orderbook = {}
cash = {'USD': 100000, 'JPY': 0, 'EUR': 0, 'CHF': 0, 'CAD': 0}
cycles = [['EURCHF', 'CHFJPY', 'EURJPY'], ['USDCAD', 'EURUSD', 'EURCAD'], ['CHFJPY', 'USDCHF', 'USDJPY']]
time_last_order = time.time()
time_last_clear = time.time()
time_last_threshold_update = time.time()

arb_threshold = 0.007
pnl_deltas = [0 for _ in range(5)]
current_pnl = 1
trans_fee = 0.0001



file = open("test.txt", 'w')
for i in tickers:
    state[i] = {}
#file = open("testfile.txt","w")
"""
EURJPY
USDCHF
EURCHF
EURCAD
"""
def get_side():
    return 'buy' if random.random() > 0.5 else 'sell'

def f(msg, order):
    global tick
    msg = msg["market_state"]
    idx = msg["ticker"]
    state[idx]["bids"] = msg['bids']
    state[idx]["asks"]  = msg['asks']
    file.write(str(msg["bids"]) + "\n")
    if state['USDCHF']:
        print(1)
        if state["EURUSD"]:
            print(2)
            arbit(order)

    tick+=1


def arbit(order):
    p1a = min(state['USDCHF']['asks'].keys())
    p1b = max(state['USDCHF']['bids'].keys())
    p2a = min(state['EURUSD']['asks'].keys())
    p2b = max(state['EURUSD']['bids'].keys())
    p1 = round((float(p1a)+float(p1b))/2,2)
    p2 = round((float(p2a)+float(p2b))/2,2)
    #quantity = min(state['USDCAD']['asks'][p1], state['EURUSD']['asks'][p2])
    #print(quantity)
    #p = abs(float(state['USDCAD']['asks'][0])-float(state['USDCAD']['asks'][0])) + float(state['USDCAD']['asks'][0])
    order.addSell('USDCHF', quantity = 200, price =p1)
    order.addBuy('EURUSD', quantity = 200, price =p2)
    order.addBuy('EURCHF', quantity = 200, price = p1+p2)

    #print(state)
    """quantity = 500
    idx = 'USDCAD'
    side = get_side()
    if side == 'buy':
        order.addBuy(idx, quantity=quantity, price=0.99)
    else:
        order.addSell(idx, quantity=quantity, price=1.01)
        """

    #print(msg['market_state'])
    #print(max(msg['market_state']['bids'].keys()))
    #print('Traded')

def g(msg, order):
    print(msg)

"""def arbit(msg, order):
    global tick
"""
#t.onMarketUpdate = f
t.onTraderUpdate = g
t.run()
