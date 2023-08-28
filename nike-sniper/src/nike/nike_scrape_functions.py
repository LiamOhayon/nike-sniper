import requests

def scrape_sizes(product_url):
    product_sizes = []
    product_response = requests.get(product_url).content
    product_response = str(product_response).split('"')

    for i in range(len(product_response)):
        if product_response[i] == "localizedSize":
            current_size = product_response[i + 2]
            product_sizes.append(current_size)

    product_sizes = list(set(product_sizes))
    product_sizes = sorted(product_sizes, key=lambda x: float(x))

    return product_sizes

