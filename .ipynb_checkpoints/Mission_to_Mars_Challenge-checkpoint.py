{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "e1eab3cd",
   "metadata": {},
   "outputs": [],
   "source": [
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "from webdriver_manager.chrome import ChromeDriverManager"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "642ce854",
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "====== WebDriver manager ======\n",
      "Current google-chrome version is 101.0.4951\n",
      "Get LATEST chromedriver version for 101.0.4951 google-chrome\n",
      "Driver [C:\\Users\\willi\\.wdm\\drivers\\chromedriver\\win32\\101.0.4951.41\\chromedriver.exe] found in cache\n"
     ]
    }
   ],
   "source": [
    "executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "66aed81c",
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_all():\n",
    "    # Initiate headless driver for deployment\n",
    "    executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "    browser = Browser('chrome', **executable_path, headless=True)\n",
    "    news_title, news_paragraph = mars_news(browser)\n",
    "    # Run all scraping functions and store results in dictionary\n",
    "    data = {\n",
    "      \"news_title\": news_title,\n",
    "      \"news_paragraph\": news_paragraph,\n",
    "      \"featured_image\": featured_image(browser),\n",
    "      \"facts\": mars_facts(),\n",
    "      \"last_modified\": dt.datetime.now()\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "807081d3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Visit the mars nasa news site\n",
    "url = 'https://redplanetscience.com'\n",
    "browser.visit(url)\n",
    "# Optional delay for loading the page\n",
    "browser.is_element_present_by_css('div.list_text', wait_time=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "ad719d26",
   "metadata": {},
   "outputs": [],
   "source": [
    "def mars_news(browser):\n",
    "    html = browser.html    \n",
    "    news_soup = soup(html, 'html.parser')\n",
    "    try:\n",
    "        slide_elem = news_soup.select_one('div.list_text')\n",
    "        slide_elem.find('div', class_='content_title')\n",
    "         # Use the parent element to find the first `a` tag and save it as `news_title`\n",
    "        news_title = slide_elem.find('div', class_='content_title').get_text()\n",
    "        news_title\n",
    "                # Use the parent element to find the paragraph text\n",
    "        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()\n",
    "        news_p\n",
    "    except AttributeError:\n",
    "        return None, None\n",
    "    return news_title, news_p "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a551cc38",
   "metadata": {},
   "source": [
    "IMAGE SCRAPING"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "19b4800e",
   "metadata": {},
   "outputs": [],
   "source": [
    "def featured_image(browser):\n",
    "    # Visit URL\n",
    "    url = 'https://spaceimages-mars.com'\n",
    "    browser.visit(url)\n",
    "    # Find and click the full image button\n",
    "    full_image_elem = browser.find_by_tag('button')[1]\n",
    "    full_image_elem.click()\n",
    "    # Parse the resulting html with soup\n",
    "    html = browser.html\n",
    "    img_soup = soup(html, 'html.parser')\n",
    "    \n",
    "    try:\n",
    "       # find the relative image url\n",
    "       img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n",
    "\n",
    "    except AttributeError:\n",
    "       return None\n",
    "    img_url_rel\n",
    "    # Use the base URL to create an absolute URL\n",
    "    img_url = f'https://spaceimages-mars.com/{img_url_rel}'\n",
    "    return img_url\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "65bbaf0b",
   "metadata": {},
   "outputs": [],
   "source": [
    " def mars_facts():\n",
    "    try:\n",
    "        #use \"read_html\" to scrape the facts table into a dataframe\n",
    "        df = pd.read_html('https://galaxyfacts-mars.com')[0]\n",
    "    except BaseException:\n",
    "        return None\n",
    "    # Assign columns and set index of dataframe\n",
    "    df.columns=['Description', 'Mars', 'Earth']\n",
    "    df.set_index('Description', inplace=True)\n",
    "\n",
    "    # Convert dataframe into HTML format, add bootstrap\n",
    "    return df.to_html()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "263ac013",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "====== WebDriver manager ======\n",
      "Current google-chrome version is 101.0.4951\n",
      "Get LATEST chromedriver version for 101.0.4951 google-chrome\n",
      "Driver [C:\\Users\\willi\\.wdm\\drivers\\chromedriver\\win32\\101.0.4951.41\\chromedriver.exe] found in cache\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "None\n"
     ]
    }
   ],
   "source": [
    "if __name__ == \"__main__\":\n",
    "    # If running as script, print scraped data\n",
    "    print(scrape_all())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "94e4f7f1",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "====== WebDriver manager ======\n",
      "Current google-chrome version is 101.0.4951\n",
      "Get LATEST chromedriver version for 101.0.4951 google-chrome\n",
      "Driver [C:\\Users\\willi\\.wdm\\drivers\\chromedriver\\win32\\101.0.4951.41\\chromedriver.exe] found in cache\n"
     ]
    }
   ],
   "source": [
    "# Import Splinter, BeautifulSoup, and Pandas\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "import pandas as pd\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "# Set the executable path and initialize Splinter\n",
    "executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "browser = Browser('chrome', **executable_path, headless=False)\n",
    "\n",
    "# Visit the mars nasa news site\n",
    "url = 'https://redplanetscience.com/'\n",
    "browser.visit(url)\n",
    "\n",
    "# Optional delay for loading the page\n",
    "browser.is_element_present_by_css('div.list_text', wait_time=1)\n",
    "\n",
    "# Convert the browser html to a soup object and then quit the browser\n",
    "html = browser.html\n",
    "news_soup = soup(html, 'html.parser')\n",
    "\n",
    "slide_elem = news_soup.select_one('div.list_text')\n",
    "\n",
    "slide_elem.find('div', class_='content_title')\n",
    "\n",
    "# Use the parent element to find the first a tag and save it as `news_title`\n",
    "news_title = slide_elem.find('div', class_='content_title').get_text()\n",
    "news_title\n",
    "\n",
    "# Use the parent element to find the paragraph text\n",
    "news_p = slide_elem.find('div', class_='article_teaser_body').get_text()\n",
    "news_p\n",
    "\n",
    "# Visit URL\n",
    "url = 'https://spaceimages-mars.com'\n",
    "browser.visit(url)\n",
    "\n",
    "\n",
    "# Find and click the full image button\n",
    "full_image_elem = browser.find_by_tag('button')[1]\n",
    "full_image_elem.click()\n",
    "\n",
    "# Parse the resulting html with soup\n",
    "html = browser.html\n",
    "img_soup = soup(html, 'html.parser')\n",
    "img_soup\n",
    "\n",
    "# find the relative image url\n",
    "img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n",
    "img_url_rel\n",
    "\n",
    "# Use the base url to create an absolute url\n",
    "img_url = f'https://spaceimages-mars.com/{img_url_rel}'\n",
    "img_url\n",
    "\n",
    "\n",
    "# ### Mars Facts\n",
    "\n",
    "df = pd.read_html('https://galaxyfacts-mars.com')[0]\n",
    "df.head()\n",
    "\n",
    "df.columns=['Description', 'Mars', 'Earth']\n",
    "df.set_index('Description', inplace=True)\n",
    "df\n",
    "\n",
    "\n",
    "df.to_html()\n",
    "\n",
    "\n",
    "# ### Hemispheres\n",
    "\n",
    "# 1. Use browser to visit the URL \n",
    "url = 'https://marshemispheres.com/'\n",
    "\n",
    "browser.visit(url)\n",
    "\n",
    "\n",
    "# 2. Create a list to hold the images and titles.\n",
    "hemisphere_image_urls = []\n",
    "\n",
    "# 3. Write code to retrieve the image urls and titles for each hemisphere.\n",
    "for hemis in range(4):\n",
    "    # Browse through each article\n",
    "    browser.links.find_by_partial_text('Hemisphere')[hemis].click()\n",
    "    \n",
    "    # Parse the HTML\n",
    "    html = browser.html\n",
    "    hemi_soup = soup(html,'html.parser')\n",
    "    \n",
    "    # Scraping\n",
    "    title = hemi_soup.find('h2', class_='title').text\n",
    "    img_url = hemi_soup.find('li').a.get('href')\n",
    "    \n",
    "    # Store findings into a dictionary and append to list\n",
    "    hemispheres = {}\n",
    "    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'\n",
    "    hemispheres['title'] = title\n",
    "    hemisphere_image_urls.append(hemispheres)\n",
    "    # Browse back to repeat\n",
    "    browser.back()\n",
    "\n",
    "# Quit browser\n",
    "browser.quit()\n",
    "# 4. Print the list that holds the dictionary of each image url and title.\n",
    "hemisphere_image_urls\n",
    " \n",
    "browser.quit()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
