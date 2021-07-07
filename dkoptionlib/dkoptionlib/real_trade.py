# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 21:45:51 2021

@author: Admin
"""

import ccxt

apiKey = ''
secret = ''

config = {'apiKey': 'EcqVv8NT-Z9DiXe4_MlN70SNiNooPr6bQTwZ7cq8',
          'secret': 'JRO4RNJ9S_b22k48AP_cOVUqiMMkSrmgJuHl9yN5',
          'headers':{
              'FTX-SUBACCOUNT': 'Casimir'}
          }

ftx = ccxt.ftx(config)


# ftx 