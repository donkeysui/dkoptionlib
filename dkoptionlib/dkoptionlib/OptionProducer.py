# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 17:00:22 2021

@author: nd
"""
from option import Option
import datetime

class OptionProducer:
    
    def __init__(self):
        pass
    
    @staticmethod
    def produce(contract_name, sigma=1, price=None):
        # BTCUSD-210625-10000-P   
        attrs = contract_name.split('-')
        symbol_pair = attrs[0]
        date = attrs[1]
        strike = attrs[2]
        otype = attrs[3]
        
        # symbol dealing
        symbol_pair = symbol_pair
        
        # date dealing
        year = int(date[0:2])
        month = int(date[2:4])
        day = int(date[4:6])
        date = datetime.datetime(year=2000+year, month=month, day=day)
        expired_time = date.timestamp()
        
        # strike dealing
        strike = float(strike)
        
        # otype dealing
        otype = otype
        
        # sigma dealing
        sigma = sigma
        
        # price dealing
        price = price
        
        res = Option(symbol_pair,
                     strike,
                     expired_time,
                     otype,
                     name=contract_name)
        
        # dealing sigma
        res.sigma_set(sigma)
        
        # dealing price
        res.price_set(price)
        
        return res
        