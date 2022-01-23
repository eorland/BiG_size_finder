#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 12:23:38 2022

@author: eliorland
"""

import requests
from bs4 import BeautifulSoup
import numpy as np

def build():
    base_url = 'https://blueingreensoho.com'
    url = 'https://blueingreensoho.com/collections/denim?filter.p.product_type=Jeans'
    site = requests.get(url)
    
    soup = BeautifulSoup(site.text, 'html.parser')

    pages = soup.find_all('span',{'class':'page'})
    page_urls = [url]
    product_links = []
    product_dict = {}
    
    for page in pages:
        content = page.find_all('a',href=True)
        for a in content:
            #print(a['href'])
            page_urls.append(base_url+a['href'])
    for link in page_urls:
        site = requests.get(link)
        soup = BeautifulSoup(site.text, 'html.parser')
        all_a = soup.find_all('a',{'class':'grid-product__link'},href=True)
        #all_a = soup.find_all('a',href=True)
        for a in all_a:
            product_links.append(base_url+a['href'])
            
    for product in product_links:
        jean = requests.get(product)
        jean_soup = BeautifulSoup(jean.text, 'html.parser')
        #price = jean_soup.find_all('div',{'class':'product-block product-block--price'})
        name = jean_soup.find_all('div',{'class':'product-section'})
        for n in name:
            jean_name = n['data-product-title']
        #name = jean_soup.find_all('data-product-title')
        
        price = jean_soup.find_all('span',class_='product__price')
        for p in price:
            p_str = p.text.replace(" ", "").replace("\n", "")
            #print(p_str)
            product_dict[jean_name] = {'price':p_str}
            #nums = [int(i) for i in p_str.split() if i.isdigit()]
            #print(p.find_all('span',class_='product__price'))
        
        table = jean_soup.find_all('div',{'class':'rte'})
        rows = []
        for t in table:
            contents = t.find_all('tr')
            for row in contents:
                rows.append(row.text.strip().replace("\n", ", "))
        sizes =  {}

        for row in rows:
            row = row.split(',') # convert string to list
            print(row)
            #key, value = row[0], [float(item.strip()) if len(item.strip())>0 else np.nan for item in row[1:]]
            key, value = row[0], row[1:]
            
            if key in sizes.keys():
                sizes[key].append(value)
                #print("key already present")
                continue
            sizes[key] = value
        
        for key, value in sizes.items():
            list_of_arrays = [np.asarray(val).reshape(-1) for val in value]
            val_list = []
            for item in list_of_arrays:
                for i in item:
                    val_list.append(i)
            
            sizes[key] = val_list

            
        product_dict[jean_name]['sizes'] = sizes
    return product_dict
