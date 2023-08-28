import requests
from bs4 import BeautifulSoup

from src.Shoe import *
from src.utils import *

headers = {
    "Host": "www.adidas.co.il:443",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def get(url: str, keywords: list):

    imgs = get_imgs("adidas")
    shoes_per_page = 0

    content = requests.get(url, headers=headers).content
    soup = BeautifulSoup(content, 'html.parser')

    span_element = soup.find('span', class_='pageofNumber')
    num_of_pages = span_element.text.strip()
    num_of_pages = int(num_of_pages.replace("מתוך", "").strip())

    for i in range(num_of_pages):

        content = requests.get(f"https://www.adidas.co.il/on/demandware.store/Sites-adidas-IL-Site/he_IL/Search-UpdateGrid?cgid=Men-sneakers&pmin=0.01&searchtrigger=shownext&start={shoes_per_page}&sz=24&selectedUrl=https%3A%2F%2Fwww.adidas.co.il%2Fon%2Fdemandware.store%2FSites-adidas-IL-Site%2Fhe_IL%2FSearch-UpdateGrid%3Fcgid%3DMen-sneakers%26pmin%3D0.01%26searchtrigger%3Dshownext%26start%3D24%26sz%3D24", headers=headers).content
        soup = BeautifulSoup(content, 'html.parser')

        details_divs = soup.find_all('div', class_='tile-body')
        image_containers = soup.find_all('div', class_='image-container')

        for shoe_details, img_container in zip(details_divs, image_containers):

            link_and_name_element = shoe_details.find('div', class_='pdp-link').find('a')
            product_url = 'https://www.adidas.co.il' + link_and_name_element['href']
            product_name = link_and_name_element.text.strip()
            price_element = shoe_details.find('div', class_='price')
            sales = price_element.find('span', class_='sales')

            if sales:
                product_price = sales.find('span', class_='value').text.strip()
            else:
                product_price = price_element.find('span', class_='value').text.strip()

            product_image = img_container.find('img', class_='tile-image image-default')['src']

            product_sizes = []
            product_content = requests.get(product_url, headers=headers).content
            soup = BeautifulSoup(product_content, 'html.parser')
            sizes_blocks = soup.find('div', class_='radio-group size-tabs')
            if sizes_blocks:
                sizes_blocks = sizes_blocks.find_all('div', class_='size-radio')

                for size_block in sizes_blocks:
                    if 'disabled' not in size_block.get('class', []):
                        current_size = size_block.find('span', class_='size-value').text
                        product_sizes.append(current_size)

            shoe = Shoe("adidas", product_name, product_url, product_price, product_image, product_sizes)

            for keyword in keywords:
                if keyword in shoe.name.lower():
                    if shoe.sizes and shoe.price:
                        if shoe.img not in imgs:
                            shoe.discord_message()
                            shoe.update()
                            imgs.append(shoe.img)
                        else:
                            check_for_updates(shoe.sizes, get_stored_sizes(shoe.site, shoe.url), shoe)

        shoes_per_page += 24
        page_url = f"https://www.adidas.co.il/on/demandware.store/Sites-adidas-IL-Site/he_IL/Search-UpdateGrid?cgid=Men-sneakers&pmin=0.01&searchtrigger=shownext&start={shoes_per_page}&sz=24&selectedUrl=https%3A%2F%2Fwww.adidas.co.il%2Fon%2Fdemandware.store%2FSites-adidas-IL-Site%2Fhe_IL%2FSearch-UpdateGrid%3Fcgid%3DMen-sneakers%26pmin%3D0.01%26searchtrigger%3Dshownext%26start%3D24%26sz%3D24"

