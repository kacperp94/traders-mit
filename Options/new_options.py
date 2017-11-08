import numpy as np
import math
from scipy.stats import norm
from operator import itemgetter


def blsc_price(S,K,r = 0.0 ,sigma,t,T):
	d1 = (math.log(S/K) + ((r + math.pow(sigma,2)/2)*(T-t)))/(sigma*math.sqrt(T-t))
	d2 = d1 - sigma*math.sqrt(T-t)
	C = norm.cdf(d1)*S - norm.cdf(d2)*K*math.exp(-r*(T-t))
	P = C + K*math.exp(-r*(T-t)) - S
	return( d1, d2, C, P )

def delta(d1, cp_flag):
	#cp_flag provides call or put information
	if cp_flag == 'C':
		return( norm.cdf(d1) )
	else:
		return( norm.cdf(d1) - 1 )

def gamma( d1, S, sigma, T, t, cp_flag):
	if cp_flag == 'C':
		return( norm.pdf(d1) / (S *sigma * math.sqrt(T-t)) )
	else:
		return( ( norm.pdf(d1) / (S *sigma * math.sqrt(T-t)) ) * norm.cdf(d1)  )

def vega( S, d1, T, t ):
	#As both call and put return same value, no need for cp_flag
	return( S * norm.pdf(d1) * math.sqrt(T-t))

def newton_vol(target_value, S, K, r=0.0, T, t, cp_flag ):
    epsilon = 1.0e-5
    num_iterations = 150
    sigma = 0.5
    for i in xrange(0, num_iterations):
        d1, blsc_price = itemgetter(*[0,1])(blsc_price( S, K,r ,sigma ,t ,T ))
        vega = vega( S, d1, T, t )
        diff = target_value - blsc_price  
        if (abs(diff) < epsilon):
            return sigma
        sigma = sigma + diff/vega 
    return sigma
    #if condition not met, return whatever sigma value computed