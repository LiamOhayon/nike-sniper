import json

def get_sizes(product_content):
    sizes = []

    product_content = json.loads(product_content)
    for size in product_content["product"]["variationAttributes"][1]["values"]:
        if size["selectable"]:
            sizes.append(size["value"])

    return sizes


