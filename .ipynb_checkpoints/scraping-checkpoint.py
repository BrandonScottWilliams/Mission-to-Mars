{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "e1eab3cd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Splinter and BeautifulSoup\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "import pandas as pd "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "642ce854",
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
    "executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "807081d3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 3,
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
   "execution_count": 4,
   "id": "ad719d26",
   "metadata": {},
   "outputs": [],
   "source": [
    "html = browser.html\n",
    "news_soup = soup(html, 'html.parser')\n",
    "slide_elem = news_soup.select_one('div.list_text')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "48b15fc5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<div class=\"content_title\">Curiosity Mars Rover's Summer Road Trip Has Begun</div>"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "slide_elem.find('div', class_='content_title')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "3f82e2df",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"Curiosity Mars Rover's Summer Road Trip Has Begun\""
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use the parent element to find the first `a` tag and save it as `news_title`\n",
    "news_title = slide_elem.find('div', class_='content_title').get_text()\n",
    "news_title"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "cfa5c580",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'After more than a year in the \"clay-bearing unit,\" Curiosity is making a mile-long journey around some deep sand so that it can explore higher up Mount Sharp.'"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use the parent element to find the paragraph text\n",
    "news_p = slide_elem.find('div', class_='article_teaser_body').get_text()\n",
    "news_p"
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
   "execution_count": 8,
   "id": "19b4800e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit URL\n",
    "url = 'https://spaceimages-mars.com'\n",
    "browser.visit(url)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "af35f89d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find and click the full image button\n",
    "full_image_elem = browser.find_by_tag('button')[1]\n",
    "full_image_elem.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "d90b5844",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Parse the resulting html with soup\n",
    "html = browser.html\n",
    "img_soup = soup(html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "475236a9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'image/featured/mars3.jpg'"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Find the relative image url\n",
    "img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n",
    "img_url_rel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "29c57df0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'https://spaceimages-mars.com/image/featured/mars3.jpg'"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use the base URL to create an absolute URL\n",
    "img_url = f'https://spaceimages-mars.com/{img_url_rel}'\n",
    "img_url\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "45271d89",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Mars</th>\n",
       "      <th>Earth</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>description</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Mars - Earth Comparison</th>\n",
       "      <td>Mars</td>\n",
       "      <td>Earth</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Diameter:</th>\n",
       "      <td>6,779 km</td>\n",
       "      <td>12,742 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Mass:</th>\n",
       "      <td>6.39 × 10^23 kg</td>\n",
       "      <td>5.97 × 10^24 kg</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Moons:</th>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Distance from Sun:</th>\n",
       "      <td>227,943,824 km</td>\n",
       "      <td>149,598,262 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Length of Year:</th>\n",
       "      <td>687 Earth days</td>\n",
       "      <td>365.24 days</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Temperature:</th>\n",
       "      <td>-87 to -5 °C</td>\n",
       "      <td>-88 to 58°C</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                    Mars            Earth\n",
       "description                                              \n",
       "Mars - Earth Comparison             Mars            Earth\n",
       "Diameter:                       6,779 km        12,742 km\n",
       "Mass:                    6.39 × 10^23 kg  5.97 × 10^24 kg\n",
       "Moons:                                 2                1\n",
       "Distance from Sun:        227,943,824 km   149,598,262 km\n",
       "Length of Year:           687 Earth days      365.24 days\n",
       "Temperature:                -87 to -5 °C      -88 to 58°C"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df = pd.read_html('https://galaxyfacts-mars.com')[0]\n",
    "df.columns=['description', 'Mars', 'Earth']\n",
    "df.set_index('description', inplace=True)\n",
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "7c77c91c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'<table border=\"1\" class=\"dataframe\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Mars</th>\\n      <th>Earth</th>\\n    </tr>\\n    <tr>\\n      <th>description</th>\\n      <th></th>\\n      <th></th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>Mars - Earth Comparison</th>\\n      <td>Mars</td>\\n      <td>Earth</td>\\n    </tr>\\n    <tr>\\n      <th>Diameter:</th>\\n      <td>6,779 km</td>\\n      <td>12,742 km</td>\\n    </tr>\\n    <tr>\\n      <th>Mass:</th>\\n      <td>6.39 × 10^23 kg</td>\\n      <td>5.97 × 10^24 kg</td>\\n    </tr>\\n    <tr>\\n      <th>Moons:</th>\\n      <td>2</td>\\n      <td>1</td>\\n    </tr>\\n    <tr>\\n      <th>Distance from Sun:</th>\\n      <td>227,943,824 km</td>\\n      <td>149,598,262 km</td>\\n    </tr>\\n    <tr>\\n      <th>Length of Year:</th>\\n      <td>687 Earth days</td>\\n      <td>365.24 days</td>\\n    </tr>\\n    <tr>\\n      <th>Temperature:</th>\\n      <td>-87 to -5 °C</td>\\n      <td>-88 to 58°C</td>\\n    </tr>\\n  </tbody>\\n</table>'"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.to_html()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "2141eb24",
   "metadata": {},
   "outputs": [],
   "source": [
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "97e24b85",
   "metadata": {},
   "outputs": [],
   "source": []
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
