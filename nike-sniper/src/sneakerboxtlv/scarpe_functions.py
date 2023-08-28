def get_image(product_soup):
    return f"{product_soup.find('img', class_='obj-f-cover prod-zoom item active').get('src')}"


def get_sizes(product_soup):
    sizes = []

    sizes_parent = product_soup.find_all('div', class_='option enabled')
    for size in sizes_parent:
        sizes.append(size.text.strip())

    return sizes

