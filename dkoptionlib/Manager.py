# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:29:02 2021

@author: nd
"""

from OptionProducer import OptionProducer
from collections import namedtuple
import datetime

test_options_list = [['btc-210808-25000-C',0.95,10],
                     ['btc-210808-25000-P',0.95,10],
                     ['btc-210808-35000-P',0.95,10],
                     ['btc-210808-15000-C',0.95,10],
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
        series = None
        option = self.__get_all()
        if not series:
            series = pd.Series(option.greeks())
        else:
            series += pd.Series(option.greeks())
        return series

    def show_by_price(price_array):
        pass
    
    # - show -
    
    
    
    
    
a = Manager()
a.read_tuple(test_options_list)