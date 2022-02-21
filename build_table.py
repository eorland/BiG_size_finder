#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 12:23:38 2022

@author: eorland
"""

import requests
from bs4 import BeautifulSoup
import numpy as np

def build():
    '''
    Function that scrapes the Blue in Green website for their jean stock
    and corresponding attributes. The patterns for pulling the requisite 
    product urls, prices, and measurements are website specific and are 
    current as of the creation of this code. 
    
    They are subject to change without warning.

    Returns
    -------
    product_dict : dictionary
        Simple dictionary storing all relevent product attributes.
    '''
    
    base_url = 'https://blueingreensoho.com'
    url = 'https://blueingreensoho.com/collections/denim?filter.p.product_type=Jeans'
    site = requests.get(url)

    soup = BeautifulSoup(site.text, 'html.parser')

    pages = soup.find_all('span',{'class':'page'})
    page_urls = [url]
    product_links = []
    product_dict = {}

    for page in pages: # all product pages(1,2,3, etc.)
        content = page.find_all('a',href=True)
        for a in content:
            page_urls.append(base_url+a['href'])
    
    for link in page_urls: # get all products from each page
        site = requests.get(link) 
        soup = BeautifulSoup(site.text, 'html.parser')
        # 'grid-product__link' == product link (go figure.)
        all_a = soup.find_all('a',{'class':'grid-product__link'},href=True)
        for a in all_a:
            product_links.append(base_url+a['href'])

    # look at each product, pull relevent info.
    for product in product_links:
        jean = requests.get(product)
        jean_soup = BeautifulSoup(jean.text, 'html.parser')
        
        name = jean_soup.find_all('div',{'class':'product-section'})
        for n in name:
            jean_name = n['data-product-title']
        
        price = jean_soup.find_all('span',class_='product__price')
        for p in price:
            # p.text contains the price but it needs to be cleaned up
            p_str = p.text.replace(" ", "").replace("\n", "")

            # add price
            product_dict[jean_name] = {'price':p_str}

        
        # get size chart rows - they're in a table under 'rte' class
        table = jean_soup.find_all('div',{'class':'rte'})
        rows = []
        for t in table:
            contents = t.find_all('tr') 

            for row in contents:
                # get each entry as comma separated value
                item = row.text.strip().replace("\n", ", ")
                rows.append(item)
        
        sizes =  {}

        # ugly code for brute force cleaning
        for row in rows:
            row = row.split(',') # convert string to list
            # keys are the jean attribute (waist, thigh, knee, tag size, etc)
            # values are the measurements for each
            key, values = row[0], [item.replace(' ','') for item in row[1:]]
            new_vals = []
            for value in values: # need to parse through each entry and clean
                # delete spaces, extra characters
                v = value.replace(' ','').replace('~','').replace('-','')
                
                # if just number, add it. replace() method to handle floats
                if v.replace('.','').isnumeric(): 
                    new_vals.append(float(v))
                
                else: # exception handling
                    if len(v)==0: # handle missing vals
                        continue
                    if len(v)>0: # handle weird alphanumeric strings
                        if v.isalpha(): # for sizes "S", "M", "L", etc.
                            new_vals.append(v)
                        else: # for cases when size is 32x32, 34x32, etc.
                            new_vals.append(float(v[:2])) # just get the waist
                    
            # back to keys, enter the cleaned measurements for each category
            if key in sizes.keys():
                sizes[key].append(new_vals)
                continue
            sizes[key] = new_vals
        
        # last cleaning step, get rid of nested arrays
        for key, value in sizes.items():
            list_of_arrays = [np.asarray(val).reshape(-1) for val in value]
            val_list = []
            for item in list_of_arrays:
                for i in item:
                    val_list.append(i)
            
            sizes[key] = val_list

            
        product_dict[jean_name]['sizes'] = sizes 
        product_dict[jean_name]['link'] = product

    return product_dict
