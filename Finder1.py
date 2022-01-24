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

class Finder:
    def __init__(self,waist,f_rise,b_rise,
                     thigh,knee,hem,inseam):
        self.waist = waist
        self.f_rise = f_rise
        self.b_rise = b_rise
        self.thigh = thigh
        self.knee = knee 
        self.hem = hem
        self.inseam = inseam
        self.Build = False

    def build(self):
        d = build()
        df = pd.DataFrame()
        for key in d.keys():
            sizes = d[key]['sizes']
            #print(sizes)
            size_df = pd.DataFrame.from_dict(sizes,orient='index')
            size_df['PRICE'] = d[key]['price']
            size_df = pd.concat({key: size_df}, names=['NAME'])
            df = pd.concat([df,size_df])
        self.products = df
        self.Build = True
    

    def find(self):
        assert self.Build==True, "use build() before find()!"
        req = pd.Series([None, self.waist, self.f_rise, self.b_rise,
                   self.thigh, self.knee, self.hem, self.inseam])
            
        return req

        
f = Finder(30,10,None,11,None,6,33)
f.build()
req = f.find()
print(req)
#d = f.products
#l = list(d.keys())[0]
#print(d[l]['link'])
#df = pd.DataFrame()
#for key in d.keys():
#    sizes = d[key]['sizes']
    #print(sizes)
#    size_df = pd.DataFrame.from_dict(d[key]['sizes'],orient='index')
#    size_df['PRICE'] = d[key]['price']
    #size_df['NAME'] = key
#    size_df = pd.concat({key: size_df}, names=['NAME'])
#    print(size_df)
#    df = pd.concat([df,size_df])
#    print('\n')
#    print(d[key]['link'])
#    sizes = d[key]['sizes']

#    print(sizes)
   # for key, value in sizes.items():
   #     print(key, "len:",len(value))

    
        
    