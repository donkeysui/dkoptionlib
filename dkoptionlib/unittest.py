# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 16:07:50 2021

@author: Admin
"""

from option import Option
import time
from numpy import exp, log, sqrt
import scipy.stats as sps
norm = sps.norm.cdf

class DebugOption(Option):
    
    def __d(self, price=None):
        
        if not price:
            price = self.price
            
        def d1(S,K,T,r,sigma):
            return(log(S/K)+(r+sigma**2/2.)*T)/sigma*sqrt(T)
        def d2(S,K,T,r,sigma):
            return d1(S,K,T,r,sigma)-sigma*sqrt(T)
        
        S = price
        K = self.strike
        T = self._Option__tau()
        r = self.r
        sigma = self.sigma
        print(S,K,T,r,sigma)

        
        return d1(S,K,T,r,sigma),d2(S,K,T,r,sigma)
    
def d1(S,K,T,r,sigma):
    return(log(S/K)+(r+sigma**2/2.)*T)/sigma*sqrt(T)
def d2(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma)-sigma*sqrt(T)

def d(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma), d2(S,K,T,r,sigma)    

def bs_call(S,K,T,r,sigma):
    return S*norm(d1(S,K,T,r,sigma))-K*exp(-r*T)*norm(d2(S,K,T,r,sigma))
  
def bs_put(S,K,T,r,sigma):
    return K*exp(-r*T)-S+bs_call(S,K,T,r,sigma)

# o1 = DebugOption('btc', 17500, time.time()+86400*80, 'P')
# o1.price_set(35000)
# o1.sigma_set(0.9)
# print(o1._Option__d())
# print(o1.greeks())
# print(1)

o1 = DebugOption('btc', 70000, time.time()+86400*80, 'C')
o1.price_set(35000)
o1.sigma_set(1)
print(o1._Option__d())
print(d(35000,70000,0.21917,0,1))
print(o1.greeks())
print(1)

# o1 = DebugOption('btc', 100, time.time()+86400*365, 'P')
# o1.price_set(100)
# o1.sigma_set(0.3)
# print(o1._Option__d())
# print(o1.greeks())
# print(1)

# o1 = DebugOption('btc', 100, time.time()+86400*365, 'C')
# o1.price_set(100)
# o1.sigma_set(0.3)
# print(o1._Option__d())
# print(o1.greeks())
# print(1)

# o1 = DebugOption('btc', 34000, time.time()+86400, 'P')
# o1.price_set(35000)
# o1.sigma_set(1)

# print(o1.greeks())

# o1 = DebugOption('btc', 10000, time.time()+86400*100, 'P')
# o1.price_set(35000)
# o1.sigma_set(1)

# print(o1._Option__d())
# print(o1.greeks())

# o1 = DebugOption('btc', 100000, time.time()+86400*100, 'C')
# o1.price_set(35000)
# o1.sigma_set(1)

# print(o1.greeks())