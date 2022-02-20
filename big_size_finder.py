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
            size_df = pd.DataFrame.from_dict(sizes,orient='index')
            size_df['PRICE'] = d[key]['price']
            size_df['LINK'] = d[key]['link']
            size_df = pd.concat({key: size_df}, names=['NAME'])
            df = pd.concat([df,size_df])
        self.products = df
        self.Build = True
    

    def find(self,waist=None,f_rise=None,b_rise=None,thigh=None,
             knee=None,hem=None,inseam=None,tol=1,return_list=False):
        assert self.Build==True, "use build() before find()!"
        req = pd.Series(['USER', waist, f_rise, b_rise,
                   thigh, knee, hem, inseam])
        
        candidates = {}
        for name in self.products.index.get_level_values(0).unique():
            #print(name)
            # work with copy of data, just easier
            copy = self.products.loc[name].copy() 
            #print(copy)
            copy['user_meas'] = req.values # set user values
            
            # remove nans and price -- items not necessary
            copy.dropna(axis=1, how='all',inplace=True) 
            copy.drop(['PRICE','LINK'],axis=1,inplace=True)
            
            
            # transpose
            t = copy.T.set_index('TAGGED SIZE')
            #print(t)
            #print('\n')
            # separate user and size info
            user = t.loc['USER']
            inventory = t.drop('USER')
            #print(user)
            # take differences 
            abs_diff = inventory.sub(user.values).abs().astype(float)
            #print(abs_diff)
            mins = pd.DataFrame(abs_diff.min(),columns=['Mins'])
            mins['idx'] = abs_diff.idxmin() # index of each min
            
            mins[mins['Mins']>tol] = np.nan # factor in tolerance
            #print(mins)
            cnts = mins['idx'].value_counts() # get counts of unique sizes
            #print(cnts)
            #print('best:',cnts.idxmax())
            if cnts.max()>=3: # if the same size is close 3 times, add it
                candidates[name] = {'Size':cnts.idxmax(),
                                    'Measurements': t.loc[cnts.idxmax()].to_string(index=True),
                                    'Price': self.products.loc[name]['PRICE'].max(),
                                    'Link': self.products.loc[name]['LINK'][0]}
                                    
        
        if len(candidates.keys())==0:
            print('No products match the specfied search criteria.')
            return 
        
        print('\nFound the following model(s):\n')
        for key in candidates.keys():
            print('\n----------------------------\n'+ # line 1
                  '\n'+str(key) + ' in size ' + str(candidates[key]['Size'])+ # line 2 pt1
                  ' ('+str(candidates[key]['Price'])+').' # line 2 pt2
                  '\n\nProduct link: '+str(candidates[key]['Link']) + # line 3
                  '\n\nSize Chart: \n\n'+ str(candidates[key]['Measurements'])) # line 4
        
        if return_list:
            return candidates
        else: 
            return

f = Finder()
f.build()
req = f.find(31.5,10.75,None,11,None,5.75,33,tol=1)

#print(req)

          
    #for keys in key:



