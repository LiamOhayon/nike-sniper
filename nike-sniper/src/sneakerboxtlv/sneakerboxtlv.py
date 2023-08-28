from bs4 import BeautifulSoup
import requests

from ..sneakerboxtlv.scarpe_functions import get_image, get_sizes
from ..utils import get_urls, get_stored_sizes, check_for_updates
from ..Shoe import Shoe
"""
SITE ALGORITHM STARTS HERE

SITE NAME: Sneakerboxtlv
"""


def get(url: str, keywords: list):
    cookies = {"tk_or": "%22%22", "tk_r3d": "%22%22", "tk_lr": "%22%22"}
    headers = {"Sec-Ch-Ua": "\"Not:A-Brand\";v=\"99\", \"Chromium\";v=\"112\"", "Accept": "*/*",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36",
                     "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://sneakerboxtlv.com",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                     "Referer": "https://sneakerboxtlv.com/product-category/footwear/",
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    offset = 0
    urls = get_urls("sneakerboxtlv")
    for i in range(12):

        data = {"action": "more_prods", "offset": f"{offset}", "productCat": "footwear", "brand": '', "gender": ''}
        content = requests.post(url, headers=headers, cookies=cookies, data=data).content
        soup = BeautifulSoup(content, 'html.parser')

        product_parents = soup.find_all('div')
        for product_children in product_parents:
            if "product" in product_children.get('class'):
                name = product_children.find('a').find('div', class_='title').text.strip().replace("                                                ", " ")
                p_url = product_children.find('a').get("href")

                for keyword in keywords:
                    if keyword in name.lower():
                        sec_content = requests.get(p_url).content
                        sec_soup = BeautifulSoup(sec_content, 'html.parser')

                        price = product_children.find('a').find('div', class_='price').text.strip()
                        sizes = get_sizes(sec_soup)
                        image = get_image(sec_soup).strip()

                        if sizes == []:
                            continue


                        shoe = Shoe("sneakerboxtlv", name, p_url, price, image, sizes)

                        if p_url not in urls:
                            shoe.discord_message()
                            shoe.update()
                            urls.append(shoe.url)
                        else:
                            check_for_updates(sizes, get_stored_sizes(shoe.site, shoe.url), shoe)

        offset += 24

