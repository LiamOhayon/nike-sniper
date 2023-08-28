def get_sizes(product_soup):
    sizes = []

    sizes_parent = product_soup.find_all('div', class_='variant-input')
    for size in sizes_parent:
        if size.find('input')['class'] != " disabled":
            sizes.append(size.find('label').text)

    return sizes

