import search as sc


def replace_with_ids(entities):
    '''
    Converts specific names in entities to reference ids in other entities
    '''
    _replace_drugs_in_ingredients_with_ids(entities)
    _replace_animals_in_combinations_with_ids(entities)
    _replace_methods_in_ingredients_with_ids(entities)


def _replace_animals_in_combinations_with_ids(entities):
    for combination in entities["combinations"]:
        animal = sc.search_animals_by_name(combination.animal, entities["animals"])
        if animal:
            combination.animal = animal.id.get()


def _replace_methods_in_ingredients_with_ids(entities):
    for ingredient in entities["ingredients"]:
        for method in ingredient.methods:
            method = sc.search_methods_by_name(method, entities["methods"])
            if method:
                ingredient.methods.remove(f"{method.name}")
                ingredient.methods.add(method.id.get())


def _replace_drugs_in_ingredients_with_ids(entities):
    '''
    Replace drug names with their correpsonding ids from the Drug class
    '''
    for ingredient in entities["ingredients"]:
        drug = sc.search_drugs_by_name(ingredient.drug, entities["drugs"])

        if drug:
            ingredient.drug = drug.id.get()



