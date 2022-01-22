#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 12:03:30 2022

@author: eliorland
"""

import requests
from bs4 import BeautifulSoup
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
    
    #table = jean_soup.find_all('div',{'class':'rte'})
print(product_dict)



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
    
    