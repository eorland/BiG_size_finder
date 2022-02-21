# BiG_size_finder
Bottom line up front: simple Python tool to find the best fitting pair of jeans at the high end denim shop, [Blue in Green (BiG)](https://blueingreensoho.com/). 

**More info:** 
There are three main stores in the United States which are well known for carrying high-end Japanese denim. 
Two of them ([Self Edge](https://www.selfedge.com/) and [Blue Owl](https://www.blueowl.us/)) have their own tools for you to enter your desired measurements and they search their inventory for the closest matches to your ideal jean. 
On the other hand, I couldn't find one on the Blue in Green website, so I made a tool to do just that. 

*This is a bare bones, web-scraper which looks at the products on their
site, records the relevent information about each product and its size run, and returns the jeans with the closest matches to your size criteria.*

Note: This tool is meant as a proof-of-concept and is only functional so long as the structure of the webpage holds. This may change at any time. I have no affiliation with BiG
and simply wanted to try to make a similar tool to those that I've seen elsewhere.

## Usage

Open your terminal or any Python IDE and run the following: 

```>>> from big_size_finder import Finder```

```>>> finder = Finder() # create finder instance```

```>>> finder.build() # scrape BiG website. Only needs to be run once.```

```>>> finder.find(waist=31.5,f_rise=11,thigh=11,inseam=34) # not all options shown```

This produces the following output (other entries ommitted for brevity):

``` 
Found the following model(s):

AI-013 17oz Natural Indigo Slim Tapered (Blue In Green Version) in size 32.0 ($659.00).

Product link: https://blueingreensoho.com/collections/denim/products/ai-013-17-5oz-natural-indigo-slim-tapered-blue-in-green-version?_pos=2&_fid=1ea331cc0&_ss=c

Size Chart: 

WAIST           31.5
FRONT RISE      11.0
BACK RISE       14.0
UPPER THIGH    11.75
KNEE             8.0
LEG OPENING     6.75
INSEAM          33.5

----------------------------

XX-18oz-019-WID Relax Tapered Jeans Blue In Green Exclusive Version in size 30.0 ($380.00).

Product link: https://blueingreensoho.com/collections/denim/products/xx-18oz-019-wid-relax-tapered-jeans-blue-in-green-exclusive-version?_pos=4&_fid=1ea331cc0&_ss=c

Size Chart: 

WAIST           30.5
FRONT RISE      11.0
BACK RISE      14.75
UPPER THIGH     12.0
KNEE            7.75
LEG OPENING      6.5
INSEAM          34.0
```
**Note: I do not plan on regularly maintaining this repo in favor of other projects. Please still create an issue for any bugs. Feel free to fork this repo and maintain as you please.**
