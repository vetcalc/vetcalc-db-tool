import csv
from operator import attrgetter


import entities as ent
import string_manipulation as sm

INPUT_CSV = "drugs.csv"

NUM_INGREDIENT_ATTR = 6 # relative to the original csv

FIRST_DRUG_NAME_COL = 3
SECOND_DRUG_NAME_COL = FIRST_DRUG_NAME_COL + NUM_INGREDIENT_ATTR
THIRD_DRUG_NAME_COL = SECOND_DRUG_NAME_COL + NUM_INGREDIENT_ATTR

def make_entities():
    entities = dict()

    # Make entities by parsing csv
    entities["animals"] = make_animals()
    entities["drugs"] = make_drugs()
    entities["methods"] = make_methods()
    entities["ingredients"] = [] # ingredients will be made later after dedup
    entities["combinations"] =  make_combinations()
      
    return entities


def make_animals():
    names = set()
    animals = []

    with open(INPUT_CSV, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            names.add(row[0])

    for name in sorted(names):
        animals.append(ent.Animal(sm.remove_whitespace(name)))

    # add on the ids
    for idx, animal in enumerate(animals):
        animal.id.set(idx+1)

    return animals


def make_drugs():
    names = set()
    drugs = []

    with open(INPUT_CSV, newline='') as csv_file:
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

    with open(INPUT_CSV, newline='') as csv_file:
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
        escaped = sm.escape_characters(to_add)
        no_whites = sm.remove_whitespace(escaped)
        a_set.add(no_whites)


def _add_ingredient(storage, row, drug_name_col):
        ingredient = _pull_ingredient(row, drug_name_col) 
        
        if ingredient:
            storage.append(ent.Ingredient(ingredient))


def _pull_ingredient(row, column):
    ingredient_info = []
    if row[column]:
        for i in range(NUM_INGREDIENT_ATTR):
            info = row[column + i]
            escaped = sm.escape_characters(info)
            no_spacing = sm.remove_whitespace(escaped)
            ingredient_info.append(no_spacing)
    return ingredient_info


def make_combinations():
    combinations = []

    with open(INPUT_CSV, newline='') as csv_file:
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

    animal = sm.remove_whitespace(animal)
    combination = ent.Combination(animal, for_juvenile)
    combination.combined_with, column = _assign_value_and_advance_column(row, column)
    
    ingredients, column = _parse_ingredients_from_combination_row(row, column)
    
    combination.purpose, column = _assign_value_and_advance_column(row, column)
    combination.notes, column = _assign_value_and_advance_column(row, column)
    combination.reference, column = _assign_value_and_advance_column(row, column)

    # add quoation marks to escape , in csv file
    combination.purpose = f"\"{combination.purpose}\""
    combination.notes = f"\"{combination.notes}\""
    combination.reference = f"\"{combination.reference}\""
    
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
    value = sm.escape_characters(row[column])
    column += 1
    return (value, column)


def _assign_ingredient_and_advance_column(row,column):
    ingredient = _pull_ingredient(row, column)
    column += NUM_INGREDIENT_ATTR
    return (ingredient, column)


