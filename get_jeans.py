#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 12:03:30 2022

@author: eliorland
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
#import BeautifulSoup

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
        row = row.split(',')
        key, values = row[0], row[1:]
        print('orig vals:', values, 'for', key)
        #print(values.replace(' ',''))# convert string to list
        new_vals = []
        for value in values:
            # delete spaces, extra characters
            v = value.replace(' ','').replace('~','').replace('-','')
            if v.isnumeric():
                new_vals.append(float(v))
            else:
                #print(v)
                if len(v)==0: # handle missing vals
                    new_vals.append(np.nan)
                if len(v)>0: # handle weird alphanumeric strings
                    if v.isalpha():
                        new_vals.append(v)
                    else:
                        new_vals.append(float(v[:2]))
                
                
        print("new vals:", new_vals)
        #key, value = row[0], [float(item.strip()) for item in row[1:]]
        if key in sizes.keys():
            sizes[key].append(new_vals)
            #print("key already present")
            continue
        sizes[key] = new_vals
    
    for key, value in sizes.items():
        list_of_arrays = [np.asarray(val).reshape(-1) for val in value]
        val_list = []
        for item in list_of_arrays:
            for i in item:
                val_list.append(i)
        
        sizes[key] = val_list

        
    product_dict[jean_name]['sizes'] = sizes

#print('this is the dev commit')


    #all_a = soup.find_all('a',{'class':'grid-product__link'},href=True)
    #all_a = soup.find_all('a',href=True)
    #a = all_a[:1][0]
    #for a in all_a:
    #    href_list.append(base_url+a['href'])
    #page_urls.append(page.find_all('a',href=True))
    #print((page.find_all('a',href=True)))
#pages = soup.find_all('div', attrs={'class': 'pagination'})
#for page in pages:
#    print(page)
    #print(page.find_all('a'))
#all_a = soup.find_all('a',{'class':'grid-product__link'},href=True)
#href_list = []
#all_a = soup.find_all('a',href=True)
#a = all_a[:1][0]
#for a in all_a:
#    href_list.append(base_url+a['href'])
    
    