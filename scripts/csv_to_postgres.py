import csv
import entities as ent
from operator import attrgetter

CSV_FILENAME = "drugs.csv"
DATABASE_IMPORT_PREFIX = "for_database_import"

NUM_INGREDIENT_ATTR = 6 # not including id

FIRST_DRUG_NAME_COL = 3
SECOND_DRUG_NAME_COL = FIRST_DRUG_NAME_COL + NUM_INGREDIENT_ATTR
THIRD_DRUG_NAME_COL = SECOND_DRUG_NAME_COL + NUM_INGREDIENT_ATTR


def main():
    entities = make_entities()
    dedup_entities(entities)
    make_references(entities)
    # show_entities(entities)
    write_all_into_csv(entities)


def dedup_entities(entities):
    '''
    denormalizes entities for sql tables
    '''
    entities["combinations"] = dedup_combinations(entities["combinations"])
    entities["ingredients"] = gather_ingredients(entities["combinations"])
    entities["ingredients"] = dedup_ingredients(entities["ingredients"])

def gather_ingredients(combinations):
    ingredients = []

    for combo in combinations:
        for a_list in combo.ingredients:
            for ingredient in a_list:
                ingredient.combination = combo.id.get()
                ingredients.append(ingredient)

    # convert methods from a string to a set
    for ingredient in ingredients:
        method = ingredient.methods
        ingredient.methods = list()
        ingredient.methods.append(method)

    # ids need setting
    for idx, ingredient in enumerate(ingredients):
        ingredient.id.set(idx+1)

    return ingredients


def make_references(entities):
    '''
    Converts specific names in entities to reference ids in other entities
    '''
    replace_drugs_in_ingredients_with_ids(entities)
    replace_animals_in_combinations_with_ids(entities)
    replace_methods_in_ingredients_with_ids(entities)


def make_entities():
    entities = dict()

    # Make entities by parsing csv
    entities["animals"] = make_animals()
    entities["drugs"] = make_drugs()
    entities["methods"] = make_methods()
    entities["ingredients"] = [] # ingredients will be made later after dedup
    entities["combinations"] =  make_combinations()
      
    return entities


def show_entities(entities):
    # Pretty print the results
    # show_items(entities["animals"], "Animals:")
    # show_items(entities["drugs"], "Drugs:")
    # show_items(entities["methods"], "Methods:")
    # show_items(entities["ingredients"], "Ingredients:")
    # show_items(entities["combinations"], "Combinations:")
    # show_detailed_combinations(entities["combinations"])

    return


def show_detailed_combinations(combinations):
    for combo in combinations:
        combo.show()
        for idx, ingredient_list in enumerate(combo.ingredients):
            print(f"List {idx}")
            [ingredient.show() for ingredient in ingredient_list]
    return 


def write_all_into_csv(entities):
    # convert the objects into rows in some csv files
    write_objects_into_csv(entities["animals"],
                            "id,name,temperature,heart_rate,respiratory_rate\n",
                            f'{DATABASE_IMPORT_PREFIX}/animals.csv'
                           )
    write_objects_into_csv(entities["drugs"],
                            "id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/drugs.csv'
                           )
    write_objects_into_csv(entities["methods"],
                            "id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/methods.csv'
                           )
    write_objects_into_csv(entities["ingredients"],
                            "id,drug,concentration,concentration_unit,dosage,dosage_unit,method\n",
                            f'{DATABASE_IMPORT_PREFIX}/ingredients.csv'
                           )
    write_objects_into_csv(entities["combinations"], 
                            "id,animal,for_juvenile,combined_with,purpose,notes,reference\n",
                           f'{DATABASE_IMPORT_PREFIX}/combinations.csv'
                           )


def write_objects_into_csv(storage, header, filename):
    with open(filename, 'w') as file:
        file.write(header) 
        for item in storage:
            file.write(item.format())


def show_items(storage, title):
    print(title)
    for item in storage:
        item.show()


def make_animals():
    names = set()
    animals = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            names.add(row[0])

    for name in sorted(names):
        animals.append(ent.Animal(remove_whitespace(name)))

    # add on the ids
    for idx, animal in enumerate(animals):
        animal.id.set(idx+1)

    return animals


def make_drugs():
    names = set()
    drugs = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_to_set(names, row[FIRST_DRUG_NAME_COL])  
            _add_to_set(names, row[SECOND_DRUG_NAME_COL])  
            _add_to_set(names, row[THIRD_DRUG_NAME_COL])  
 
    for drug in sorted(names):
        drugs.append(ent.Drug(drug))

    # add on the ids
    for idx, drug in enumerate(drugs):
        drug.id.set(idx+1)

    return drugs


def make_methods():
    names = set()
    methods = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_to_set(names, row[FIRST_DRUG_NAME_COL + 5])  
            _add_to_set(names, row[SECOND_DRUG_NAME_COL + 5])  
            _add_to_set(names, row[THIRD_DRUG_NAME_COL + 5])  
 
    for method in sorted(names):
        methods.append(ent.Method(method))

    # add on the ids
    for idx, method in enumerate(methods):
        method.id.set(idx+1)

    return methods


def _add_to_set(a_set, to_add):
    if to_add:
        a_set.add(remove_whitespace(to_add))


def _add_ingredient(storage, row, drug_name_col):
        ingredient = _pull_ingredient(row, drug_name_col) 
        
        if ingredient:
            storage.append(ent.Ingredient(ingredient))


def _pull_ingredient(row, column):
    ingredient_info = []
    if row[column]:
        for i in range(NUM_INGREDIENT_ATTR):
            info = row[column + i]
            no_spacing = remove_whitespace(info)
            ingredient_info.append(no_spacing)
    return ingredient_info


def remove_whitespace(item):
    try:
        item = "".join(item.split())
    except:
        pass
    finally:
        return item


def make_combinations():
    combinations = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            _add_combination(combinations, row)
    
    sorted_combinations = sorted(combinations, key=attrgetter("animal", "for_juvenile"))
    
    # add on the ids
    for idx, combination in enumerate(sorted_combinations):
        combination.id.set(idx+1)

    return sorted_combinations


def _add_combination(storage, row):

    column = 0
    animal, column = _assign_value_and_advance_column(row, column) 
    for_juvenile, column = _assign_value_and_advance_column(row, column)
    if for_juvenile:
        for_juvenile = True
    else:
        for_juvenile = False

    animal = remove_whitespace(animal)
    combination = ent.Combination(animal, for_juvenile)
    combination.combined_with, column = _assign_value_and_advance_column(row, column)
    
    ingredients, column = _parse_ingredients_from_combination_row(row, column)
    
    combination.purpose, column = _assign_value_and_advance_column(row, column)
    combination.notes, column = _assign_value_and_advance_column(row, column)
    combination.reference, column = _assign_value_and_advance_column(row, column)
  
    
    actual_ingredients = []
    for ingredient in ingredients:
        if ingredient:
            actual_ingredients.append(ent.Ingredient(ingredient))

    combination.add_ingredients(actual_ingredients)

    storage.append(combination)


def _parse_ingredients_from_combination_row(row, column):
    ingredients = []
    
    ingredient, column = _assign_ingredient_and_advance_column(row, column)
    ingredients.append(ingredient)
    
    ingredient, column = _assign_ingredient_and_advance_column(row, column)
    ingredients.append(ingredient)
    
    ingredient, column = _assign_ingredient_and_advance_column(row, column)
    ingredients.append(ingredient)

    return (ingredients, column)


def _assign_value_and_advance_column(row, column):
    value = row[column]
    column += 1
    return (value, column)


def _assign_ingredient_and_advance_column(row,column):
    ingredient = _pull_ingredient(row, column)
    column += NUM_INGREDIENT_ATTR
    return (ingredient, column)


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


def replace_animals_in_combinations_with_ids(entities):
    for combination in entities["combinations"]:
        animal = search_animals_by_name(combination.animal, entities["animals"])
        if animal:
            combination.animal = animal.id.get()


def replace_methods_in_ingredients_with_ids(entities):
    for ingredient in entities["ingredients"]:
        for idx, method in enumerate(ingredient.methods):
            method = search_methods_by_name(method, entities["methods"])
            if method:
                ingredient.methods[idx] = method.id.get()


def replace_drugs_in_ingredients_with_ids(entities):
    '''
    Replace drug names with their correpsonding ids from the Drug class
    '''
    for ingredient in entities["ingredients"]:
        drug = search_drugs_by_name(ingredient.drug, entities["drugs"])

        if drug:
            ingredient.drug = drug.id.get()


def dedup_ingredients(ingredients):
    '''
    combine similar ingredients together 
    '''
    normalized = []

    for ingredient in ingredients:
        add_to_normalized_ingredients(ingredient, normalized)

    for idx, ingredient in enumerate(normalized):
        ingredient.id.set(idx+1)

    return normalized


def add_to_normalized_ingredients(ingredient, normalized):
    match_idx = contains_ingredient(ingredient, normalized)
    if match_idx == -1:
        normalized.append(ingredient)
    else:
        for method in ingredient.methods:
            normalized[match_idx].methods.append(method)


def contains_ingredient(ingredient, a_list):
    if not a_list:
        return -1
    
    for idx, an_ingredient in enumerate(a_list):
        if ingredients_match(ingredient, an_ingredient):
            return idx

    return -1


def ingredients_match(first, second):
    if first.combination != second.combination:
        return False
    if first.drug != second.drug:
        return False
    if remove_whitespace(first.concentration) != remove_whitespace(second.concentration):
        return False
    if remove_whitespace(first.concentration_unit) != remove_whitespace(second.concentration_unit):
        return False
    if remove_whitespace(first.dosage) != remove_whitespace(second.dosage):
        return False
    if remove_whitespace(first.dosage_unit) != remove_whitespace(second.dosage_unit):
        return False
    return True


def dedup_combinations(combinations):
    '''
    Look through combinations and combine similar combinations
    by filtering into a second list
    '''
    normalized = []

    for combination in combinations:
        add_to_normalized_combinations(combination, normalized)

    for idx, combination in enumerate(normalized):
        combination.id.set(idx+1)

    return normalized

def add_to_normalized_combinations(combination, normalized):
    match_idx = contains_combination(combination, normalized)
    if match_idx == -1:
        normalized.append(combination)
    else:        
        for ingredient_list in combination.ingredients:
            normalized[match_idx].ingredients.append(ingredient_list)


def contains_combination(combination, a_list):
    if not a_list:
        return -1
    
    for idx, a_combo in enumerate(a_list):
        if combinations_match(combination, a_combo):
            return idx

    return -1
   

def combinations_match(combo_1, combo_2):
    if combo_1.animal != combo_2.animal:
        return False
    if combo_1.for_juvenile != combo_2.for_juvenile:
        return False
    if remove_whitespace(combo_1.combined_with) != remove_whitespace(combo_2.combined_with):
        return False
    if remove_whitespace(combo_1.purpose) != remove_whitespace(combo_2.purpose):
        return False
    if remove_whitespace(combo_1.notes) != remove_whitespace(combo_2.notes):
        return False
    if remove_whitespace(combo_1.reference) != remove_whitespace(combo_2.reference):
        return False
    if not ingredient_lists_match(combo_1.ingredients, combo_2.ingredients):
        return False
    return True


def ingredient_lists_match(list_1, list_2):
    # there must be the same number of ingredients
    if len(list_1[0]) != len(list_2[0]):
        return False

    # and the names must match
    names = set()
    for ingredient in list_1[0]:
        names.add(ingredient.drug)

    for ingredient in list_2[0]:
        if ingredient.drug not in names:
            return False

    return True

if __name__ == "__main__":
    main()
