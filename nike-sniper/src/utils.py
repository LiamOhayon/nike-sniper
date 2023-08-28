import json


def get_urls(site: str):
    urls = []

    product_data_file = json.load(open("./data.json", "r"))
    for product in product_data_file[site]:
        urls.append(product["url"])

    return urls

def get_imgs(site: str):
    imgs = []

    product_data_file = json.load(open("./data.json", "r"))
    for product in product_data_file[site]:
        imgs.append(product["img"])

    return imgs

def get_stored_sizes(site, url):
    with open("./data.json", 'r+') as file:
        file_data = json.load(file)
        for stored_shoe in file_data[site]:
            if stored_shoe["url"] == url:
                return stored_shoe["sizes"]



def check_for_updates(sizes, stored_sizes, shoe):
    if len(sizes) > len(stored_sizes):
        added = [i for i in sizes if i not in stored_sizes]
        shoe.update_sizes(sizes)
        if len(stored_sizes) == 0:
            shoe.discord_message()
        else:
            shoe.update_sizes_message(added_sizes=added, removed_sizes=[])

    elif len(sizes) < len(stored_sizes):
        removed = [i for i in stored_sizes if i not in sizes]
        if len(removed) == len(stored_sizes):
            shoe.update_sizes(sizes)
        else:
            shoe.update_sizes(sizes)
            shoe.update_sizes_message(added_sizes=[], removed_sizes=removed)
