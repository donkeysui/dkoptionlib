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

N = sps.norm.cdf

class Option:
    
    def __init__(self,symbol,strike,expired_time,otype):
        self.symbol = symbol
        self.strike = strike
        self.expired_time = expired_time
        self.otype = otype
        self.r = 0
        self.now_time = time.time()
        
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
                }
        
    # - utils -
    
    def __tau(self, now_time=None):
        if not now_time:
            now_time = time.time()
        return (self.expired_time - self.now_time)/86400/365
    
    def __d(self, price=None):
        if not price:
            price = self.price
        self.d_1 = (np.log(price / self.strike) 
        + (self.r -  .5 * self.sigma ** 2) 
        * self.__tau()) / self.sigma / np.sqrt(self.__tau())
        self.d_2 = self.d_1 - self.sigma * np.sqrt(self.__tau())
        return self.d_1,self.d_2
    
    # - greeks - 
    def __delta(self, price=None):
        if not price:
            price = self.price
        
        if self.otype == 'C':
            delta = N(self.__d(price)[0])
        elif self.otype == 'P':
            delta = N(self.__d(price)[0]) - 1
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
        sign = (self.otype=='C')
        d1, d2 = self.__d(price)
        p = sign *price * np.e ** (-self.r * self.__tau()) * N(d1*sign) - \
            sign * self.strike * np.e**(-self.r*self.__tau()) * N(d2)
        return p
        
        
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
        
    # - functions -
    