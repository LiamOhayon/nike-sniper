from bs4 import BeautifulSoup
import requests
import json

from ..utils import get_urls, get_stored_sizes, check_for_updates
from ..Shoe import Shoe
from ..notforsale.scrape_functions import get_sizes

"""
SITE ALGORITHM STARTS HERE

SITE NAME: not for sale
"""

def get(url: str, keywords: list):
    try:

        pages = [url + '1']

        content = requests.get(url + '1').content
        soup = BeautifulSoup(content, 'html.parser')
        page_num = int(soup.find('div', class_='pagination').find('a').text)

        for page in range(1, page_num + 1):
            pages.append(f'{url}{page}')

        urls = get_urls("notforsale")

        for page in pages:
            content = requests.get(page).content
            soup = BeautifulSoup(content, 'html.parser')
            product_parent = soup.find_all('div', class_='grid-product__content')
            for product_child in product_parent:

                p_url = f"https://notforsaletlv.com/{product_child.find('a')['href']}"
                image = f"https:{product_child.find('img')['src']}"
                name = f"{product_child.find('div', class_='grid-product__meta').find('div', class_='grid-product__vendor').text.strip()} {product_child.find('div', class_='grid-product__meta').find('div', class_='grid-product__title grid-product__title--heading').text.strip()}"
                price = product_child.find('div', class_='grid-product__price').text.strip().split('\n')

                if "Regular price" in price:
                    price = price[2][10:]
                else:
                    price = price[0]

                for keyword in keywords:
                    if keyword in name.lower():
                        sec_content = requests.get(p_url).content
                        sec_soup = BeautifulSoup(sec_content, 'html.parser')
                        sizes = get_sizes(sec_soup)
                        shoe = Shoe("notforsale", name, p_url, price, image, sizes)

                        if p_url not in urls:
                            shoe.discord_message()
                            shoe.update()
                            urls.append(shoe.url)
                        else:
                            check_for_updates(sizes, get_stored_sizes(shoe.site, shoe.url), shoe)
    except Exception:
        pass

