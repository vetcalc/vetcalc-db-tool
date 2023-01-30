import csv
import entities as ent
from operator import attrgetter

CSV_FILENAME = "drugs.csv"
DATABASE_IMPORT_PREFIX = "for_database_import"

NUM_INGREDIENT_ATTR = 6

FIRST_DRUG_NAME_COL = 3
SECOND_DRUG_NAME_COL = FIRST_DRUG_NAME_COL + NUM_INGREDIENT_ATTR
THIRD_DRUG_NAME_COL = SECOND_DRUG_NAME_COL + NUM_INGREDIENT_ATTR

def main():
    entities = make_entities()
    make_references(entities)
    show_entities(entities)
    split_entities_into_csv(entities)

def make_references(entities):
    '''
    Converts specific names in entities to reference ids in other entities
    '''
    replace_ingredient_attributes_with_ids(entities)
    

def make_entities():
    entities = dict()

    # Make entities by parsing csv
    entities["animals"] = make_animals()
    entities["drugs"] = make_drugs()
    entities["ingredients"] = make_ingredients()
    entities["combinations"] =  make_combinations()
    
    return entities

def show_entities(entities):
    # Pretty print the results
    show_items(entities["animals"], "Animals:")
    show_items(entities["drugs"], "Drugs:")
    show_items(entities["ingredients"], "Ingredients:")
    show_items(entities["combinations"], "Combinations:")

def split_entities_into_csv(entities):
    # split the main csv into smaller files ready for imporation
    split_animals_into_csv(entities["animals"])
    split_drugs_into_csv(entities["drugs"])
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
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            names.add(row[0])

    for name in sorted(names):
        animals.append(ent.Animal(name))

    return animals

def make_drugs():
    names = set()
    drugs = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_drug(names, row[FIRST_DRUG_NAME_COL])  
            _add_drug(names, row[SECOND_DRUG_NAME_COL])  
            _add_drug(names, row[THIRD_DRUG_NAME_COL])  
 
    for drug in sorted(names):
        drugs.append(ent.Drug(drug))

    return drugs

def _add_drug(a_set, to_add):
    if to_add:
        a_set.add(to_add)

def make_ingredients():
    ingredients = []

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_ingredient(ingredients, row, FIRST_DRUG_NAME_COL)  
            _add_ingredient(ingredients, row, SECOND_DRUG_NAME_COL)  
            _add_ingredient(ingredients, row, THIRD_DRUG_NAME_COL)  

    return sorted(ingredients, key=attrgetter("drug", "concentration", "dosage", "method"))

def _add_ingredient(storage, row, drug_name_col):
    if row[drug_name_col]:
        ingredient_info = []

        for i in range(NUM_INGREDIENT_ATTR):
            ingredient_info.append(row[drug_name_col + i])

        storage.append(ent.Ingredient(ingredient_info))

def make_combinations():
    return []

def split_animals_into_csv(storage):
    '''
    Write the animals found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/animals.csv', 'w') as file:
        header = "id,name,temperature,heart_rate,respiratory_rate\n"
        file.write(header) 

        for idx, animal in enumerate(storage):
            animal.id.set(idx+1)
            row = (f"{animal.id.get()},"
                   f"{animal.name},"
                   f"{animal.temperature},"
                   f"{animal.heart_rate},"
                   f"{animal.respiratory_rate}\n"
                  )
            file.write(row)

def split_drugs_into_csv(storage):
    '''
    Write the drugs found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/drugs.csv', 'w') as file:
        header = "id,name\n"
        file.write(header) 

        for idx, drug in enumerate(storage):
            drug.id.set(idx+1)
            row = (f"{drug.id.get()},"
                   f"{drug.name}\n"
                  )
            file.write(row)

def split_ingredients_into_csv(storage):
    '''
    Write the ingredients found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/ingredients.csv', 'w') as file:
        header = "id,drug,concentration,concentration_unit,dosage,dosage_unit,method\n"
        file.write(header) 

        for idx, ingredient in enumerate(storage):
            ingredient.id.set(idx+1)
            row = (f"{ingredient.id.get()},"
                   f"{ingredient.drug},"
                   f"{ingredient.concentration},"
                   f"{ingredient.concentration_unit},"
                   f"{ingredient.dosage},"
                   f"{ingredient.dosage_unit},"
                   f"{ingredient.method},\n"
                  )
            file.write(row)

def split_combinations_into_csv(storage):
    '''
    Write the ingredients found into their own csv file with unique ids
    '''
    with open(f'{DATABASE_IMPORT_PREFIX}/combinations.csv', 'w') as file:
        header = "id,animal,for_juvenile,combined_with,drug1,drug2,drug3,purpose,notes,reference\n"
        file.write(header) 

        for idx, combination in enumerate(storage):
            combination.id.set(idx+1)
            row = (f"{combination.id.get()}\n"
                  )
            file.write(row)

def search_drugs_by_name(name, drugs):
    for drug in drugs:
        if drug.name == name:
            return drug.id
    # no match
    return ""

def replace_ingredient_attributes_with_ids(entities):
    '''
    Replace drug names with their correpsonding ids from the Drug class
    '''

    for ingredient in entities["ingredients"]:
        drug_id = search_drugs_by_name(ingredient.drug, entities["drugs"])
        if drug_id.is_set():
            ingredient.drug = {drug_id.get()}

def replace_combination_attributes_with_ids(entities):
    '''
    Take the original csv, which has no concept of ids for each entity (execept combinations)
    and replace the objects with their corresponsding ids from the various make_ commands.

    This will reduce the number of colunmns as compared to the original csv
    '''
    pass    
    # reduced_combinations = []

    # with open(CSV_FILENAME, newline='') as csv_file:
    #     reader = csv.reader(csv_file, quotechar='|') 
        # for idx, row in enumerate(reader):
        #     if idx == 0:
        #         continue # ignore the header
            # replace



if __name__ == "__main__":
    main()
