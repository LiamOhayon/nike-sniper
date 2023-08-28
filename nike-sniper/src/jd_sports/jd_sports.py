from bs4 import BeautifulSoup
import requests

from ..jd_sports.scarpe_functions import get_price, get_image, get_sizes
from ..Shoe import Shoe
from ..utils import get_urls, get_stored_sizes, check_for_updates


"""
SITE ALGORITHM STARTS HERE

SITE NAME: JD Sports
"""


def get(urls: str, keywords: list):
    for url in urls:
        for i in range(12):
            urls = get_urls("jd_sports")

            content = requests.get(url + str(i)).content
            soup = BeautifulSoup(content, 'html.parser')
            product_parents = soup.find_all('div', class_='product-item-meta')

            for product_children in product_parents:
                name = product_children.find('h2', class_='product-item-meta__title').text.strip()
                for keyword in keywords:
                    if keyword in name.lower():
                        product_id = product_children.find('h2', class_='product-item-meta__title').find('a').get('href').split('/')[-1]

                        p_url = f"https://www.jdsports.co.il/products/{product_id}".strip()

                        sec_content = requests.get(p_url).content
                        sec_soup = BeautifulSoup(sec_content, 'html.parser')

                        price = get_price(sec_soup)
                        sizes = get_sizes(sec_soup)
                        image = get_image(sec_soup)

                        shoe = Shoe("jd_sports", name, p_url, price, image, sizes)

                        if p_url not in urls:
                            shoe.discord_message()
                            shoe.update()
                            urls.append(shoe.url)
                        else:
                            check_for_updates(sizes, get_stored_sizes(shoe.site, shoe.url), shoe)



