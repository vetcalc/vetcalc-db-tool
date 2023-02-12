def search_drugs_by_name(name, drugs):
    for drug in drugs:
        if drug.name == name:
            return drug
    return ""


def search_animals_by_name(name, animals):
    for animal in animals:
        if animal.name == name:
            return animal
    return ""


def search_ingredient_by_info(info, ingredients):
    for ingredient in ingredients:
        if ingredient.matches(info):
            return ingredient
    return ""


def search_methods_by_name(name, methods): 
    for method in methods:
        if method.name == name:
            return method
    return ""



