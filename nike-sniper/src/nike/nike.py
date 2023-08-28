from src.nike import nike_scrape_functions

import requests
from bs4 import BeautifulSoup
import concurrent.futures
from src.Shoe import Shoe
from src.utils import *

ANCHOR_OFFSET = 24
NOT_EXIST = -1

def process_api_product_info(product):
    full_url = "https://www.nike.com/il" + product['url'][13:]
    product_price = product["price"]["currentPrice"]
    product_name = product["title"]
    product_image = product["images"]["portraitURL"]
    product_sizes = nike_scrape_functions.scrape_sizes(full_url)


    if not product_sizes:
        return None

    return Shoe("nike", product_name, full_url, product_price, product_image, product_sizes)



def get(link: str, keywords: list):

    nike_urls = {
        'men': f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=CFD2FD8E39261E9F8455D413E1597666&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D",
        'women': 'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=3B92F143E7E35F9BC32752892407F7BF&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C7baf216c-acc6-4452-9e07-39c2ca77ba32)%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D',
        'kids': 'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=3B92F143E7E35F9BC32752892407F7BF&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C145ce13c-5740-49bd-b2fd-0f67214765b3)%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D'
    }

    anchor = 0
    urls = get_urls("nike")

    for key, url in nike_urls.items():
        while True:
            updated_url = url.replace('anchor%3D0%', f'anchor%3D{anchor}%')
            response = requests.get(updated_url)
            api_data = response.json()

            products = api_data["data"]["products"]["products"]

            for product in products:
                shoe = process_api_product_info(product)

                if shoe:
                    for keyword in keywords:
                        if keyword.lower() in shoe.name.lower():
                            if shoe.url not in urls:
                                shoe.discord_message()
                                shoe.update()
                                urls.append(shoe.url)

            anchor += ANCHOR_OFFSET
            updated_url = updated_url.replace(f'anchor%3D{anchor - ANCHOR_OFFSET}%', f'anchor%3D{anchor}%')

            if len(products) < ANCHOR_OFFSET:
                break

