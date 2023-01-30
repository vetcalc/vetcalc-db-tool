import csv
import entities as ent

CSV_FILENAME = "drugs.csv"
DATABASE_IMPORT_PREFIX = "for_database_import"

NUM_INGREDIENT_ATTR = 6

FIRST_DRUG_NAME_COL = 3
SECOND_DRUG_NAME_COL = FIRST_DRUG_NAME_COL + NUM_INGREDIENT_ATTR
THIRD_DRUG_NAME_COL = SECOND_DRUG_NAME_COL + NUM_INGREDIENT_ATTR

def main():
    make_entities()
    show_entities()
    split_entities_into_csv()

def make_entities():
    # Make entities by parsing csv
    animals = make_animals()
    drugs = make_drugs()
    ingredients = make_ingredients()
    combinations =  make_combinations()

def show_entities():
    # Pretty print the results
    show_items(animals, "Animals:")
    show_items(drugs, "Drugs:")
    show_items(ingredients, "Ingredients:")
    show_items(combinations, "Combinations:")

def split_entities_into_csv():
    # split the main csv into smaller files ready for imporation
    split_animals_into_csv(animals)
    split_drugs_into_csv(drugs)
    split_ingredients_into_csv(ingredients)
    split_combinations_into_csv(combinations)


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

    for name in names:
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
 
    for drug in names:
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

    return ingredients

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
            resource_prefix = "a_"
            row = (f"{resource_prefix}{idx+1},"
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
            resource_prefix = "d_"
            row = (f"{resource_prefix}{idx+1},"
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
            resource_prefix = "i_"
            row = (f"{resource_prefix}{idx+1},"
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
            resource_prefix = "c_"
            row = (f"{resource_prefix}{idx+1}\n"
                  )
            file.write(row)

if __name__ == "__main__":
    main()
