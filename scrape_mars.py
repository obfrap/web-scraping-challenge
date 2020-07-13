# Imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from splinter.exceptions import ElementDoesNotExist
import requests
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #Mars dict to hold info
    mars_data={}
    
    # Get Mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    # find new news article titles
    news_title = soup.find("div",class_="content_title").text
    # find new news articles text
    news_text = soup.find("div", class_="article_teaser_body").text
    
    #Get Mars img from JPL
    jpl_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_images_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    img_source = soup.find(class_ = "carousel_item")['style']
    # Use split to get the text portion just related to the full size image URL.
    string_split = img_source.split("'")[0]
    image_split = img_source.split("'")[1]
    # Combine with base url to make complete url for image
    featured_image_url = jpl_images_url + image_split
    
    #Twitter scrape
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path)
    twit_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twit_url)
    
    # Use find by css method with click to access tweet.  Tried with beautiful soup in jupyter notebook
    # Resource website used https://www.seleniumeasy.com/selenium-tutorials/css-selectors-tutorial-for-selenium-with-examples
    browser.find_by_css('div[class="css-1dbjc4n r-1awozwy r-18u37iz r-1wtj0ep"]').first.click()
    #find and save text from tweet.  End up in [6] location
    target_tweet = browser.find_by_css('span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]')[6].text
    
    #Mars Facts Scrape
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_facts_df = pd.read_html(facts_url)[0]
    mars_facts_df.columns=["Facts", "Values"]
    mars_facts_df.set_index("Facts", inplace=True)
    mars_facts_html = mars_facts_df.to_html()
    
    # Mars Hemispheres
    mars_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemi_url)
    hemi_img_url = []
    links = browser.find_by_css("a.product-item h3")
    n = len(links)
    
    for row in range(n):
        hemi_dict = {}
        browser.find_by_css("a.product-item h3")[row].click()
    
        sample_element = browser.find_link_by_text("Sample").first
    
        # Update dictionary with image url and title
        hemi_dict["img_url"] = sample_element["href"]
        hemi_dict["title"] = browser.find_by_css("h2.title").text
    
        # Append it to 
        hemi_img_url.append(hemi_dict)
    
        # Need to send browser back each time in order to click each product-item.
        browser.back()
        
        #Update mars_data with information
    mars_data = {
            "mars_news_title": news_title,
            "mars_news_teaser": news_text,
            "mars_tweet": target_tweet,
            "mars_image": featured_image_url,
            "mars_table": mars_facts_html,
            "hemi_image_title_1": hemi_img_url[0]["title"],
            "hemi_image_url_1": hemi_img_url[0]["img_url"],
            "hemi_image_title_2": hemi_img_url[1]["title"],
            "hemi_image_url_2": hemi_img_url[1]["img_url"],
            "hemi_image_title_3": hemi_img_url[2]["title"],
            "hemi_image_url_3": hemi_img_url[2]["img_url"],
            "hemi_image_title_4": hemi_img_url[3]["title"],
            "hemi_image_url_4": hemi_img_url[3]["img_url"]      
        }
    browser.quit()
        
    return mars_data
   
    
    
    
    