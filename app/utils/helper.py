def generate_sku(category, brand, product, model=None):
    SKU = [category[:4]]

    SKU.append(brand[:4])
    product_code = generate_product_code(product)
    SKU.append(product_code)
    if model:
        SKU.append(model)
    
    return "-".join(SKU).upper()


def generate_product_code(product_name:str):
    product_name = product_name.strip()
    print(product_name)
    if " " not in product_name:
        return product_name[:4]
    
    product_code = ""
    words = product_name.split(" ")
    for word in words :
        product_code+= word[:4]

    return product_code

