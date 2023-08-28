def get_price(product_soup):
    return ''.join(filter(lambda x: x.isdigit() or x == '.', product_soup.find('div', class_='row_2tcG bold_2wBM prices-final_1R9x').text.strip()))


def get_image(product_soup):
    return product_soup.find('div', class_='image-div_3hfI').find('img').get('src')


def get_sizes(product_soup):
    sizes = []
    all_sizes = product_soup.find_all('div', class_='size-item_1Sai rtl_3a50')
    for size in all_sizes:
        if size.get('data-test-id') == "qa-size-item":
            sizes.append(size.text.strip())
    return sizes

