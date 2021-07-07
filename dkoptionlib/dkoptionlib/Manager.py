# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:29:02 2021

@author: nd
"""

from OptionProducer import OptionProducer
from collections import namedtuple
from option import Futures
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class Manager:
    
    producer = OptionProducer
    #option = namedtuple('option', ['name','sigma','position'])
    option = namedtuple('position',['option','amount'])
    
    def __init__(self):
        self.position = []
        self.futures = 0
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
    
    def greeks(self, price=None):
        series = ''
        options = self.__get_all()

        for idx in range(len(options)):
            if len(series) == 0:
                series = pd.Series(options[idx].greeks(price)) * self.position[idx].amount
            else:
                series += pd.Series(options[idx].greeks(price))  * self.position[idx].amount
        return series
    
    def show_greeks(self):
        
        options = self.__get_all()
        for idx in range(len(options)):
            print ('#' * 15 + ' ' +
                   options[idx].name +
                   ' ' + '#' * 25
                   )
            print()
            print(pd.Series(options[idx].greeks()))
            print()

    def show_by_price(price_array):
        pass
    
    def plot_time_pass(self, time_pass, now_price=None, X=None):
        
        if now_price is None:
            now_price = self.price
        if X is None:
            X = np.arange(now_price-5000,
                          now_price+5000,
                          100)
        self.price_set(now_price)
        now_position_balance = self.greeks()['price']
        self.time_change(time_pass)
        res_dict = {}
        for x in X:
            self.price_set(x)
            res_dict[x] = self.greeks()['price']
            
        res = pd.Series(res_dict) - now_position_balance
        
        interval = get_interval(res)
        print(interval)
        near_prices = res.loc[now_price-interval:now_price+interval]
        diff_prices = near_prices.diff()
        dropna_diff = diff_prices.dropna()
        mean_diff = dropna_diff.mean()
        print(near_prices, diff_prices, dropna_diff, mean_diff)
        now_delta = mean_diff / interval
        
        return res, now_delta
    
    def rehedge(self, price):
        self.price_set(price)
        return - self.greeks()['delta']
    
    # - show -
    
def get_interval(series):
    return pd.Series(series.index).diff().mean()

def futures_pnl_generate(arange, amount, price):
    
    futures = Futures(price)
    
    return (arange - price) * amount
    
def straddle_pnl_generate(arange, strike, amount, price):
    return (price - abs(arange - strike)) * amount

def find_roots(List):
    
    res = []
    
    for i in range(len(List)-1):
        if List.iloc[i] * List.iloc[i+1] < 0:
            if abs(List.iloc[i]) < abs(List.iloc[i+1]):
                res.append(List.index[i])
            else:
                res.append(List.index[i+1])
    return res

def find_new_roots(old_roots, List, donk=0.75):
    
    if not len(old_roots) == 2:
        raise ValueError('old_roots amount->({}) wrong'.format(len(old_roots)))
        
    old_roots_distance = max(old_roots) - min(old_roots)
    mid_point = np.mean(old_roots)
    
    return [mid_point - old_roots_distance * donk / 2,
            mid_point + old_roots_distance * donk / 2]

        
if __name__ == '__main__':
    
    a = Manager()
    a.read_tuple(test_options_list)
    a.price_set(35000)
    
    now_price = 35000
    now_pnl = a.greeks()['price']
    
    prices_range = range(30000,40000,100)
    
    now_dict = {}
    next_dict = {}
    
    a.time_change(86400)
    
    for price in prices_range:
        a.price_set(price)
        now_dict[price] = a.greeks()['price']
        
    a.time_change(40000)
    
    for price in prices_range:
        a.price_set(price)
        next_dict[price] = a.greeks()['price']
    
    next_day_pnl_for_otm = pd.Series(now_dict) - now_pnl
    
    plt.plot(next_day_pnl_for_otm)
    #plt.plot(pd.Series(next_dict) - now_pnl)
    plt.plot(prices_range, 0 * np.ones(100))
    
