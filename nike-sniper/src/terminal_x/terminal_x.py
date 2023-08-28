from bs4 import BeautifulSoup
import requests

from .scrape_functions import get_price, get_image, get_sizes
from ..utils import get_urls, get_stored_sizes, check_for_updates
from ..Shoe import Shoe

""" TERMINAL X """

def get(url: str, keywords: list):
    for i in range(17):

        urls = get_urls("terminal_x")

        content = requests.get(f"{url}{i+1}").content
        soup = BeautifulSoup(content, 'html.parser')
        product_parents = soup.find_all('div', class_='img-link_29yX new-listing-product_2S9n')

        for product_children in product_parents:
            name = product_children.get('title')
            for keyword in keywords:
                if keyword in name.lower():
                    p_url = f"https://www.terminalx.com/men/shoes/sneakers-shoes{product_children.find('a').get('href')}"

                    sec_content = requests.get(p_url).content
                    sec_soup = BeautifulSoup(sec_content, 'html.parser')
                    price = get_price(sec_soup).strip()
                    sizes = get_sizes(sec_soup)
                    image = get_image(sec_soup).strip()

                    shoe = Shoe("terminal_x", name, p_url, price, image, sizes)

                    if p_url not in urls:
                        shoe.discord_message()
                        shoe.update()
                        urls.append(p_url)
                    else:
                        check_for_updates(sizes, get_stored_sizes(shoe.site, shoe.url), shoe)

