#!/usr/bin/env python
# coding: utf-8

# In[15]:


import time 
from splinter import Browser 
from bs4 import BeautifulSoup as bs 
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests as req
import re
import pprint



# In[16]:


executable_path = {'executable_path' : 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[17]:


def scrape_all():
    url = "https://mars.nasa.gov/news/"
    response = req.get(url)
#     html = browser.html
    soup = bs(response.text, 'html5lib')


    # # NASA News From Mars

    # In[18]:


    news_url = "https://mars.nasa.gov/news/"
    news_browser = webdriver.Chrome()
    news_browser.get(news_url)
    time.sleep(1)
    news_titles = news_browser.find_elements_by_tag_name('a')
    news_bodies = news_browser.find_elements_by_class_name('article_teaser_body')
    all_titles = []
    all_bodies = []

    for title in news_titles: 
        all_titles.append(title.text)
    for body in news_bodies:
        all_bodies.append(body.text)
        
    news_browser.quit()


    # In[26]:


    news_title = all_titles[34]
    news_desc = all_bodies[0]

    print(news_title)
    print(news_desc)


    # # Mars Space Images 

    # In[30]:


    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url_pre_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_pre_image)


    # In[31]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[32]:


    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)


    # In[33]:


    browser.click_link_by_partial_text("more info")


    # In[34]:


    final_image_html = browser.html
    final_image_soup = bs(final_image_html, 'html.parser')
    final_image_url = final_image_soup.find('img', class_='main_image')
    url_part_two = final_image_url.get('src')
    print(url_part_two)


    # In[35]:


    featured_image_link = "https://www.jpl.nasa.gov" + url_part_two

    print(featured_image_link)
    browser.quit()


    # # Weather on Mars

    # In[36]:


    twitter_url = "https://twitter.com/marswxreport?lang=en"
    twitter_browser = webdriver.Chrome()


    # In[37]:


    twitter_browser.get(twitter_url)
    time.sleep(1)


    # In[39]:


    twitter_browser.get(twitter_url)
    time.sleep(1)


    # In[40]:


    twitter_body = twitter_browser.find_element_by_tag_name('body')


    # In[44]:


    tweets = twitter_browser.find_elements_by_class_name('tweet-text')
    mars_weathers = []
    for tweet in tweets:
        mars_weathers.append(tweet.text)
        print(tweet.text)
    twitter_browser.quit()


    # In[45]:


    current_mars_weather = mars_weathers[0]
    current_mars_weather


    # In[48]:


    url_facts = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(url_facts)

    mars_df = mars_tables[0]
    mars_df.columns = ['0', '1']
    mars_df = mars_df.iloc[0:]

    # In[50]:


    table_object = mars_df.to_html(classes="table table-striped")
    table_object = table_object.replace('\n', '')
    table_object


    # In[51]:


    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_request = req.get(usgs_url)


    # In[54]:


    usgs_soup = bs(usgs_request.text, "html.parser")
    hemisphere_list = usgs_soup.find_all('a', class_='itemLink product-item')


    # In[56]:


    hemisphere_link_1 = hemisphere_list[0]['href']
    hemisphere_link_2 = hemisphere_list[1]['href']
    hemisphere_link_3 = hemisphere_list[2]['href']
    hemisphere_link_4 = hemisphere_list[3]['href']

    print(hemisphere_link_1)
    print(hemisphere_link_2)
    print(hemisphere_link_3)
    print(hemisphere_link_4)


    # In[59]:


    hemisphere_url = 'https://astrogeology.usgs.gov'
    cerberus_url = hemisphere_url + hemisphere_link_1
    schiaparelli_url = hemisphere_url + hemisphere_link_2
    syrtis_url = hemisphere_url + hemisphere_link_3
    valles_url = hemisphere_url + hemisphere_link_4
    urls = [cerberus_url, schiaparelli_url, syrtis_url, valles_url]

    print(urls[0])
    print(urls[1])
    print(urls[2])
    print(urls[3])


    # In[61]:


    images = []
    headers = []
    for url in urls:
        image_request = req.get(url)
        image_soup = bs(image_request.text, 'html.parser')
        image_item = image_soup.find('img', class_='wide-image')
        images.append(hemisphere_url+image_item['src'])
        title = image_soup.find('h2', class_='title')
        headers.append(title.text)
        
    print(images)


    # In[62]:


    hemisphere_image_urls = [{'title':headers[0], 'img_url': images[0]},
                        {'title':headers[1], 'img_url': images[1]},
                        {'title':headers[2], 'img_url': images[2]},
                        {'title':headers[3], 'img_url': images[3]},
                    ]
    print(hemisphere_image_urls)


    # In[63]:


    mars_data_dictionary = {"News_Title": news_title,
                    "News_Description": news_desc,
                    "Featured_Image": featured_image_link,
                    "Mars_Weather": current_mars_weather,
                    "Mars_Facts": table_object,
                    "Hemispheres" : hemisphere_image_urls
                    }


    # In[64]:

    return mars_data_dictionary

