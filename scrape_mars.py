from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)
    #executable_path = {"executable_path": 'C:\Users\nsomm\.wdm\drivers\chromedriver\' }
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    title_list = []
    img_url_list = []
    o_url_list = []
    img_url_full_list = []
    hemi_img_urls = []
    img_dict = {}

    browser = init_browser()

    # Visit mars.nasa.gov/news/ and get headlines
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the headlines
    artlist = soup.find('ul', class_='item_list')
    articles = artlist.find('li')

    #first entry should be the latest one
    # scrape the article title 
    news_title = articles.find('div', class_='content_title').text
    
    # scrape the article teaser
    news_p = articles.find('div', class_='article_teaser_body').text
    
    # scrape the datetime
    #date = articles.find('div', class_='list_date').text

    #vist the nasa and get full size image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    baseurl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(url)

    time.sleep(10)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #get the image
    #header = soup.find('div', class_='header')
    image =soup.find('img', class_='fancybox-image').get('src')

    featured_image_url = baseurl + image
    print(featured_img_url)
    #get the table from this site
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    table_df = tables[0]
    #string for display
    table_html = table_df.to_html(classes='data', header="true", index="false")

    #Get the images on this page
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    #get image list on page
    sidebar = soup.find('div', class_='result-list')
    himages = sidebar.find_all('div', class_='item')


    for y in himages:
        title = y.find('h3').text
        title_list.append(title)
        img_url = y.find('a')['href']
        img_url_list.append(img_url)

    o_url_list = ['https://astrogeology.usgs.gov/' + url for url in img_url_list]

    
    for z in o_url_list:
        browser.visit(z)
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        img_url_full = downloads.find('a')['href']
        img_url_full_list.append(img_url_full)

    for p in range(len(title_list)):
        img_dict = {'title':title_list[p],
                'img_url': img_url_full_list[p]}
        hemi_img_urls.append(img_dict)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "table_html": table_html,
        "hemisphere_img_urls": hemi_img_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
