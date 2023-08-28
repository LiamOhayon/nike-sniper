import json
import time

def get_price(product_soup):
    if product_soup.find('span', class_='price price--large'):
        return ''.join(filter(lambda x: x.isdigit() or x == '.', product_soup.find('span', class_='price price--large').text))
    elif product_soup.find('span', class_='price price--highlight price--large'):
        return ''.join(filter(lambda x: x.isdigit() or x == '.', product_soup.find('span', class_='price price--highlight price--large').text))


def get_image(product_soup):
    product_image = ""
    try:
        product_image = f"https://{product_soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:]}"
    except:
        print("Error scraping image")
        time.sleep(5)
        pass
    return product_image


def get_sizes(product_soup):
    sizes = []
    try:
        for size in json.loads(product_soup.find('script', type='application/ld+json').text)['offers']:
            if size['availability'] == 'https://schema.org/InStock':
                sizes.append(size['name'].split(' / ')[0])
    except:
        print("Error scraping sizes")
        time.sleep(5)
        pass

    return sizes


