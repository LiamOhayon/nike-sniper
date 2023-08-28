import requests
from bs4 import BeautifulSoup
import concurrent.futures
from src.Shoe import Shoe
from src.utils import *
import re
import time

"""
SITE ALGORITHM STARTS HERE

SITE NAME: Foot Locker
"""


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "sh0TEc%2FhRIA2kiThL%2FFBcoWeM6i9YR77gXFBYVT0qzfL6gp%2FAiASG0AeA8HKOmsbvRylzYH8DzDfrlLZyQC3yU80NYnZ4yXcjJlQiRxsINGstqSCJyyNNUtsJqGpcr%2FrzXmaknXhtXxIweajrCMab4cJhBlTtIGLxJfqF4O9o4MqS9swE%2BWXaRYv%2B%2BH67i7sd9m%2BUnn%2BUmuPJgd6KKI%2FuSNI5P%2FLqMsi7qn5LG2Ff5XnFsIChEb8b8A9SowXWHJ59P2yEHL5KgI4J46gShrp9%2F2xBz3Cfjfg7UZBfqBqrfPfstvSbI7rUjXSqui%2Fgqd95rtdLT%2B1Ung62DDfEQ9257cshWW%2FlZxZGx0qLBtfvOIsk1gy4SLblgW7xSauXg%3D%3D",
    "sec-ch-ua": r"\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "document",
    "sec-fetch-site": "same-origin",
    "sec-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
}






def scrape_details(product_url):

    response = requests.get(product_url, headers=headers).content

    soup = BeautifulSoup(response, 'html.parser')
    product_name = soup.find('div', class_='product-right ng-star-inserted').find('h1', class_='product-name ng-star-inserted').text
    product_sizes = []
    product_img = ''
    price_element = soup.find('div', class_='discount ng-star-inserted')
    if price_element:
        product_price = price_element.find('h3').text.replace('₪', '').strip()
    else:
        if soup.find('div', class_='price ng-star-inserted').find('div', class_='ng-star-inserted').find('h3'):
            product_price = soup.find('div', class_='price ng-star-inserted').find('div', class_='ng-star-inserted').find('h3').text
        else:
            return None

    img_element = soup.find('div', class_='_ngcontent-serverapp-c9')

    if img_element:
        style_attribute = img_element['style']
        product_img = style_attribute.split('url("')[1].split('")')[0]

    size_container = soup.find('div', class_='container-size')
    size_elements = size_container.find_all('div', class_='p-size has-tooltip ng-star-inserted')
    size_elements.append(size_container.find('div', class_='p-size has-tooltip ng-star-inserted chosen'))

    for size_element in size_elements:
        if size_element:
            eu_size = size_element.find('span').text
            product_sizes.append(eu_size)

    return Shoe('footlocker', product_name, product_url, product_price, product_img, product_sizes)

def get(url: str, keywords: list):
    urls = []


    for keyword in keywords:

        offset = 0
        first_response = requests.get(f'https://www.footlocker.co.il/api/v1/search?name={keyword}&offset={offset}', headers=headers).content
        print(f'https://www.footlocker.co.il/api/v1/search?name={keyword}&offset={offset}')
        data = json.loads(first_response)

        total_count = int(data['products']['total_count'])

        for i in range((total_count // 16) + 1):
            url = f'https://www.footlocker.co.il/api/v1/search?name={keyword}&offset={offset}'
            response = str(requests.get(url, headers=headers).content.decode())
            pattern = r'"id":"([^"]+)"\s*,\s*"sku_model":"([^"]+)"'
            shoes_per_page = 0
            matches = re.findall(pattern, response)

            for match in matches:
                id = match[0]
                sku_model = match[1]
                product_url = f'https://www.footlocker.co.il/{sku_model}/prd/{id}'
                shoes_per_page += 1

                shoe = scrape_details(product_url)
                if shoe:
                    if "נעלי" in shoe.name  or "סניקרס" in shoe.name or "נעליים" in shoe.name:
                        if shoe.url not in urls:
                            print(shoe.name)
                            print(shoe.url)
                            print(shoe.img)
                            print(shoe.price)
                            print(shoe.sizes)
                            #shoe.discord_message()
                            #shoe.update()
                            #urls.append(shoe.url)
                        else:
                            X = 2
                            #check_for_updates(shoe.sizes, get_stored_sizes(shoe.site, shoe.url), shoe)

            offset += shoes_per_page


get('', ['air'])

