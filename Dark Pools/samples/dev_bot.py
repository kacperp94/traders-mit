import tradersbot as tt
import math
import random

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')
tick = 0
tickers = ['USDCAD','USDJPY','EURUSD','USDCHF','CHFJPY','EURJPY','EURCHF','EURCAD' ]

#file = open("testfile.txt","w")
def get_side():
    return 'buy' if random.random() > 0.5 else 'sell'

def f(msg, order):
    global tick
    """quantity = 500
    idx = 'USDCAD'
    side = get_side()
    if side == 'buy':
        order.addBuy(idx, quantity=quantity, price=0.99)
    else:
        order.addSell(idx, quantity=quantity, price=1.01)
        """
    tick += 1
    print(msg['market_state']['bids'])
    print(max(msg['market_state']['bids'].keys()))
    #print('Traded')

"""def arbit(msg, order):
    global tick
"""
t.onMarketUpdate = f
t.run()
