# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initialize headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    def mars_news(browser):

        # Visit the Mars NASA News site
        url = 'http://mars.nasa.gov/news/'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

        # Convert the browser html to a soup object and then quit the browser
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')

        # Add try/except for error handling
        try:
            slide_elem = news_soup.select_one('ul.item_list li.slide')
            # Use the parent element to find the first `a` tag and save it as `news_title`
            news_title = slide_elem.find("div", class_='content_title').get_text()
            # Use the parent element to find the paragraph text
            news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
            return news_title, news_p
        except AttributeError:
            return None, None    


    # ### Featured Images

    def featured_image(browser):
        # Visit URL
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()

        # Find the more info button and click that
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.links.find_by_partial_text('more info')
        more_info_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        try:
            # Find the relative image url
            img_url_rel = img_soup.select_one('figure.lede a img').get("src")
            # Use the base URL to create an absolute URL
            img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        
        except AttributeError:
            return None
        
        return img_url

    # ### Mars Facts
    def mars_facts():
        # Add try/except for error handling.
        try:
            # Use 'read_html' to scrape the facts table into a df.
            df = pd.read_html("http://space-facts.com/mars/")[0]
        
        except BaseException:
            return None

        # Assign columns and set index of dataframe.
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)

        # Convert DF back to HTML-ready code, add bootstrap.
        return df.to_html()

    ### Mars Hemispheres
    def hemi_images(browser):
        hemi_list=[]
        for x in range(0,4):
            # Visit URL
            url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
            browser.visit(url)
            
            # Find and click the full image button
            thumb_image_elem = browser.find_by_css("img.thumb")[x]
            thumb_image_elem.click()

            # Parse the resulting html with soup
            html = browser.html
            img_soup = BeautifulSoup(html, 'html.parser')

            # Find the relative image url
            img_url_rel = img_soup.select_one('img.wide-image').get("src")
            # Use the base URL to create an absolute URL
            img_url = f'https://astrogeology.usgs.gov{img_url_rel}'
            # Get title text
            title=browser.find_by_css("h2.title").first.value

            img_dict = {'img_url': img_url,'title': title}
            hemi_list.append(img_dict.copy())

        return hemi_list

# Use mars_news function to pull the data.
    news_title, news_paragraph = mars_news(browser)
    #print(hemi_images(browser))
    # Run all scraping functions and store results in dictionary
    data = {
      "hemi_images": hemi_images(browser),
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())





