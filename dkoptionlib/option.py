# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 17:00:22 2021

@author: nd
"""

import pandas as pd
import numpy as np
import datetime
import time
import scipy.stats as sps
from numpy import exp, log, sqrt

N = sps.norm.cdf

class Futures:
    
    def __init__(self, price_buy):
        self.price_buy = price_buy
    
    def greeks(self, price=None):
        
        return {'delta':1,
                'gamma':0,
                'vega':0,
                'theta':0,
                'price': price - self.price_buy}

class Option:
    
    def __init__(self,symbol,strike,expired_time,otype,name=None):
        self.symbol = symbol
        self.strike = strike
        self.expired_time = expired_time
        self.otype = otype
        self.r = 0
        self.now_time = time.time()
        self.name = name
        
    def __repr__(self):
        return '{0} | vol:{1}% | strike:{2} | type:{3}'.format(self.symbol,
                                                self.sigma*100,
                                                self.strike,
                                                self.otype)
        
    # - public functions -
    def greeks(self, price=None):
        if not price:
            price = self.price
            
        return {'delta':self.__delta(price), 
                'gamma':self.__gamma(price),
                'vega':self.__vega(price),
                'theta':self.__theta(price),
                'price':self.__price(price),
                'new_price':self.__new_price(price),
                }
        
    # - utils -
    
    def __tau(self, now_time=None):
        if not now_time:
            now_time = time.time()
        return (self.expired_time - self.now_time)/86400/365
    
    # def __d(self, price=None):
    #     if not price:
    #         price = self.price
            
    #     self.d_1 = (np.log(price / self.strike) 
    #     + (self.r -  .5 * self.sigma ** 2) 
    #     * self.__tau()) / self.sigma / np.sqrt(self.__tau())
        
    #     self.d_2 = self.d_1 - self.sigma * np.sqrt(self.__tau())
        
    #     return self.d_1,self.d_2
    
    def __d(self, price=None):
        
        if not price:
            price = self.price
            
        def d1(S,K,T,r,sigma):
            return(log(S/K)+(r+sigma**2/2.)*T)/sigma*sqrt(T)
        def d2(S,K,T,r,sigma):
            return d1(S,K,T,r,sigma)-sigma*sqrt(T)
        
        S = price
        K = self.strike
        T = self.__tau()
        r = self.r
        sigma = self.sigma
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        return d1,d2
    
    # - greeks - 
    def __delta(self, price=None):
        if not price:
            price = self.price
        
        if self.otype == 'C':
            delta = N(self.__d(price)[0])
        elif self.otype == 'P':
            delta = -N(-self.__d(price)[0])
        else:
            raise ValueError('Option Type Error ->',self.otype)
        return delta
    
    def __gamma(self,price=None):
        if not price:
            price = self.price
        d1 = self.__d(price)[0]
        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-d1 ** 2 * 0.5)
        gamma = prob_density / (price * self.sigma * np.sqrt(self.__tau()))
        return gamma
    
    def __theta(self, price=None):
        if not price:
            price = self.price
        d1, d2 = self.__d(price)
        T = self.__tau()
        sigma = self.sigma
        r = self.r
        K = self.strike
        S = price
        sign = int(self.otype=='C')
        
        prob_density = np.e ** -(d1**2/2) / np.sqrt(2*np.pi)
        theta = -S*prob_density*sigma / (2 * T**0.5) - \
                r * K * np.e ** (-r*T) * N(d2)
        return theta
    
    def __vega(self, price=None):
        if not price:
            price = self.price
        d1, _ = self.__d(price)
        prob_density = np.e ** -(d1**2/2) / np.sqrt(2*np.pi)
        vega = price * prob_density * self.__tau()**0.5
        return vega
    
    def __price(self,price=None):
        if not price:
            price = self.price
            
        print(price)
            
            
            
        sign = 1 if self.otype=='C' else -1
        d1, d2 = self.__d(price)
        p = sign *price * np.e ** (-self.r * self.__tau()) * N(d1*sign) - \
            sign * self.strike * np.e**(-self.r*self.__tau()) * N(d2*sign)
        return p
    
    def __new_price(self, price=None):
        
        if not price:
            price = self.price
        d1, d2 = self.__d(price)
        
        if self.otype=='C':
            C = N(d1) * price - N(d2) * self.strike * np.e**(-self.r * self.__tau())
            return C
        elif self.otype=='P':
            C = N(d1) * price - N(d2) * self.strike * np.e**(-self.r * self.__tau())
            P = self.strike * np.exp(-self.r*self.__tau()) - price + C
            return P
        
    # - time functions -
    def time_set(self, timestamp):
        self.now_time = timestamp
    
    def time_change(self, seconds):
        self.now_time += seconds
        
    # - sigma functions -
    def sigma_set(self, sigma):
        self.sigma = sigma
        
    def sigma_change(self, change):
        self.sigma += change
        
    # - price functions -
    def price_set(self, price):
        self.price = price
        
    def price_change(self, change):
        self.price += change
        
    # - set the expired time -
    def expired_set(self, timestamp):
        self.expired_time = timestamp        
        
    # - functions -
    