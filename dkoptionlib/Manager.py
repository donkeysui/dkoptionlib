# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:29:02 2021

@author: nd
"""

from OptionProducer import OptionProducer
from collections import namedtuple
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

test_options_list = [['btc-210623-35000-C',0.90,-.15],
                     ['btc-210623-35000-P',0.90,-.15],
                     ['btc-210908-17500-P',0.95,4.95],
                     ['btc-210908-70000-C',0.95,1.85],
                     ]

class Manager:
    
    producer = OptionProducer
    #option = namedtuple('option', ['name','sigma','position'])
    option = namedtuple('position',['option','amount'])
    
    def __init__(self):
        self.position = []
    # - private util -
    
    def __get_all(self) -> list:
        tmp_list = []
        for idx in range(len(self.position)):
            tmp_list.append(self.position[idx][0])
        return tmp_list
    
    def __operate_all(self, func_name, *args):
        options = self.__get_all()
        for option in options:
            func = getattr(option, func_name)
            func(*args)
    
    # - add options -
    
    def __add(self, option_name, sigma, amount):
        tmp_option = self.producer.produce(option_name, sigma)
        self.position.append(self.option(tmp_option, amount))
        
    def add(self, option_name: str, sigma: float, amount: float):
        self.__add(option_name, sigma, amount)
        
    def read_tuple(self, options: dict):
        # {option_name:sigma}
        for List in options:
            tmp_option = self.producer.produce(*List[:2])
            self.position.append(self.option(tmp_option, List[2]))
        return len(options)
    
    # - truncate options -
    
    def truncate(self) -> int:
        now_position_length = len(self.position)
        self.position = []
        return now_position_length
    
    # - change environment
    
    def price_set(self, price:float):
        self.__operate_all('price_set', price)
        
    def price_change(self, price:float):
        self.__operate_all('price_change', price)
    
    def time_set(self, time:float):
        self.__operate_all('time_set', time)
        
    def time_change(self, time:float):
        self.__operate_all('time_change', time)
            
    # - calculate -
    
    def show_greeks(self):
        series = ''
        options = self.__get_all()

        for idx in range(len(options)):
            if len(series) == 0:
                series = pd.Series(options[idx].greeks()) * self.position[idx].amount
            else:
                series += pd.Series(options[idx].greeks())  * self.position[idx].amount
        return series

    def show_by_price(price_array):
        pass
    
    # - show -
    
    
    
    
    
a = Manager()
a.read_tuple(test_options_list)
a.price_set(35000)

now_price = 35000
now_pnl = a.show_greeks()['price']

prices_range = range(30000,40000,100)

now_dict = {}

a.time_change(86400)

for price in prices_range:
    a.price_set(price)
    now_dict[price] = a.show_greeks()['price']


plt.plot(pd.Series(now_dict) - now_pnl)
plt.plot(prices_range, 0 * np.ones(100))

