# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:46:07 2021

@author: Admin
"""

from Manager import Manager
from Manager import (get_interval,
                     futures_pnl_generate,
                     straddle_pnl_generate,
                     find_roots,
                     find_new_roots
                     )

import numpy as np
import pandas as pd
import time
from matplotlib import pyplot as plt

test_options_list = [['btc-210709-35000-C',0.75,-.15],
                     ['btc-210709-35000-P',0.75,-.15],
                     ['btc-211231-18000-P',0.99,3],
                     ['btc-211231-70000-C',0.99,1],
                     ]

main = Manager()
main.read_tuple(test_options_list)
main.price_set(35000)

hedged_price = 35000
calculate_time_range = np.arange(30000,40000,100)
time_pass = 86400

# init position price

init_price = main.greeks(hedged_price)['price']

# calculate next
next_day_pnl, delta = main.plot_time_pass(time_pass, hedged_price)

# hedge delta from futures
futures_pnl = futures_pnl_generate(calculate_time_range, -delta, hedged_price)
next_day_pnl_hedged = next_day_pnl + futures_pnl

# choose a specific position to hedge

roots = find_roots(next_day_pnl_hedged)
new_roots = find_new_roots(roots, next_day_pnl_hedged, donk=0.70)

new_roots_pnls = []

new_roots_pnls = pd.Series([main.greeks(root)['price'] for root in new_roots])

futures_pnl_to_fix = futures_pnl_generate(pd.Series(new_roots), -delta, hedged_price) + new_roots_pnls

new_roots_hedged_pnls = futures_pnl_to_fix - init_price

atm_pnl = straddle_pnl_generate(np.array(new_roots), hedged_price, 1, 1200)

hedged_amount = (new_roots_hedged_pnls / atm_pnl).mean()
atm_all_pnl = straddle_pnl_generate(calculate_time_range, 
                                    hedged_price, 
                                    hedged_amount,
                                    1200
                                    )

atm_options_list = [['btc-210709-35000-C',0.95, hedged_amount],
                    ['btc-210709-35000-P',0.95, hedged_amount]]

expired_time = time.time() + 86400

straddle_position = Manager()
straddle_position.read_tuple(atm_options_list)
straddle_position.price_set(35000)

for option in straddle_position.position:
    option[0].expired_set(expired_time)
    
res, new_delta = straddle_position.plot_time_pass(86300,35000)















