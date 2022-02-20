#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 20:19:22 2022

@author: eliorland
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 12:17:23 2022

@author: eliorland
"""

#import requests
#from bs4 import BeautifulSoup
#import numpy as np
from build_table import build
import pandas as pd
import numpy as np

class Finder:
    def __init__(self):
        self.Build = False

    def build(self):
        d = build()
        df = pd.DataFrame()
        for key in d.keys():
            sizes = d[key]['sizes']
            #print(sizes)
            size_df = pd.DataFrame.from_dict(sizes,orient='index')
            print(size_df)
            size_df['PRICE'] = d[key]['price']
            size_df = pd.concat({key: size_df}, names=['NAME'])
            df = pd.concat([df,size_df])
        self.products = df
        self.Build = True
    

    def find(self,waist,f_rise,b_rise,thigh,knee,hem,inseam,tol=1):
        assert self.Build==True, "use build() before find()!"
        req = pd.Series(['USER', waist, f_rise, b_rise,
                   thigh, knee, hem, inseam])
        
        candidates = {}
        for name in self.products.index.get_level_values(0).unique():
            
            # work with copy of data
            copy = self.products.loc[name].copy() 
            
            copy['user_meas'] = req.values # set user values
            
            # remove nans and price -- items not necessary
            copy.dropna(axis=1, how='all',inplace=True) 
            copy.drop('PRICE',axis=1,inplace=True) 
            
            # transpose
            t = copy.T.set_index('TAGGED SIZE')
            
            # separate user and size info
            user = t.loc['USER']
            inventory = t.drop('USER')
            
            # take differences 
            abs_diff = inventory.sub(user.values).abs().astype(float)
            #mins = abs_diff.min()
            #mins[mins<tol] = np.nan
            #mins_idx = abs_diff.idxmin() # get sizes of closest values
            mins = pd.DataFrame(abs_diff.min(),columns=['Mins'])
            mins['idx'] = abs_diff.idxmin()
            mins[mins['Mins']>tol] = np.nan
            cnts = mins.value_counts() # get counts of unique sizes
            if cnts.max()>=3: # if the same size is close 3 times, add it
                candidates[name] = {'size':cnts.idxmax()[1],
                                    'measurements': t.loc[cnts.idxmax()[1]],
                                    'Price': self.products.loc[name]['PRICE'].max()}
            
            
        return candidates

        
f = Finder()
f.build()
req = f.find(30,10,None,11,None,6,33)
print(req)