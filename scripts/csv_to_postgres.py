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
    make_references(entities)
    # show_entities(entities)
    split_entities_into_csv(entities)


def make_references(entities):
    '''
    Converts specific names in entities to reference ids in other entities
    '''
    replace_ingredient_attributes_with_ids(entities)
    replace_animals_in_combinations_with_ids(entities)


def make_entities():
    entities = dict()

    # Make entities by parsing csv
    entities["animals"] = make_animals()
    entities["drugs"] = make_drugs()
    entities["methods"] = make_methods()
    entities["ingredients"] = make_ingredients()
    entities["combinations"] =  make_combinations(entities)
    
    return entities


def show_entities(entities):
    # Pretty print the results
    show_items(entities["animals"], "Animals:")
    show_items(entities["drugs"], "Drugs:")
    show_items(entities["methods"], "Methods:")
    show_items(entities["ingredients"], "Ingredients:")
    show_items(entities["combinations"], "Combinations:")


def split_entities_into_csv(entities):
    # split the main csv into smaller files ready for imporation
    split_animals_into_csv(entities["animals"])
    split_drugs_into_csv(entities["drugs"])
    split_methods_into_csv(entities["methods"])
    split_ingredients_into_csv(entities["ingredients"])
    split_combinations_into_csv(entities["combinations"])


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


def make_ingredients():
    ingredients = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_ingredient(ingredients, row, FIRST_DRUG_NAME_COL)  
            _add_ingredient(ingredients, row, SECOND_DRUG_NAME_COL)  
            _add_ingredient(ingredients, row, THIRD_DRUG_NAME_COL)  

    sorted_ingredients = sorted(ingredients, key=attrgetter("drug", "concentration", "dosage", "method"))
    # add on the ids
    for idx, ingredient in enumerate(sorted_ingredients):
        ingredient.id.set(idx+1)

    return sorted_ingredients


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


def make_combinations(entities):
    combinations = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            _add_combination(combinations, row, entities)
    
    sorted_combinations = sorted(combinations, key=attrgetter("animal", "for_juvenile"))
    # add on the ids
    for idx, combination in enumerate(sorted_combinations):
        combination.id.set(idx+1)

    return sorted_combinations


def _add_combination(storage, row, entities):

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
  
    for ingredient in ingredients:
        match = search_ingredient_by_info(ingredient, entities["ingredients"])
        if match:
            combination.add_ingredient(match.id.get())

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


def split_animals_into_csv(storage):
    '''
    Write the animals found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/animals.csv', 'w') as file:
        header = "id,name,temperature,heart_rate,respiratory_rate\n"
        file.write(header) 

        for idx, animal in enumerate(storage):
           file.write(animal.format())


def split_drugs_into_csv(storage):
    '''
    Write the drugs found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/drugs.csv', 'w') as file:
        header = "id,name\n"
        file.write(header) 

        for idx, drug in enumerate(storage):
            file.write(drug.format())


def split_methods_into_csv(storage):
    '''
    Write the methods found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/methods.csv', 'w') as file:
        header = "id,name\n"
        file.write(header) 

        for idx, method in enumerate(storage):
           file.write(method.format())


def split_ingredients_into_csv(storage):
    '''
    Write the ingredients found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/ingredients.csv', 'w') as file:
        header = "id,drug,concentration,concentration_unit,dosage,dosage_unit,method\n"
        file.write(header) 

        for idx, ingredient in enumerate(storage):
            file.write(ingredient.format())


def split_combinations_into_csv(storage):
    '''
    Write the ingredients found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/combinations.csv', 'w') as file:
        header = "id,animal,for_juvenile,combined_with,purpose,notes,reference\n"
        file.write(header) 

        for idx, combination in enumerate(storage):
            file.write(combination.format())

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


def replace_animals_in_combinations_with_ids(entities):
    for combination in entities["combinations"]:
        animal = search_animals_by_name(combination.animal, entities["animals"])
        if animal:
            combination.animal = animal.id.get()


def replace_ingredient_attributes_with_ids(entities):
    '''
    Replace drug names with their correpsonding ids from the Drug class
    '''
    for ingredient in entities["ingredients"]:
        drug = search_drugs_by_name(ingredient.drug, entities["drugs"])

        if drug:
            ingredient.drug = drug.id.get()


if __name__ == "__main__":
    main()
