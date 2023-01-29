import csv
import entities as ent

CSV_FILENAME = "drugs.csv"

NUM_INGREDIENT_ATTR = 6

FIRST_DRUG_NAME_COL = 3
SECOND_DRUG_NAME_COL = FIRST_DRUG_NAME_COL + NUM_INGREDIENT_ATTR
THIRD_DRUG_NAME_COL = SECOND_DRUG_NAME_COL + NUM_INGREDIENT_ATTR

g_animals = []
g_drugs = []
g_ingredients = []
g_combinations = []

# TODO: convert starting csv into csv with ingredients, drugs, and animals by id

def main():
   
    # Make entities by parsing csv
    make_animals(g_animals)
    make_drugs(g_drugs)
    make_ingredients(g_ingredients)
    make_combinations(g_combinations)

    # Pretty print the results
    show_items(g_animals, "Animals:")
    show_items(g_drugs, "Drugs:")
    show_items(g_ingredients, "Ingredients:")
    show_items(g_combinations, "Combinations:")

def show_items(storage, title):
    print(title)
    for item in storage:
        item.show()

def make_animals(storage):
    names = set()

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            names.add(row[0])

    for name in names:
        storage.append(ent.Animal(name))

def make_drugs(storage):
    drugs = set()

    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_drug(drugs, row[FIRST_DRUG_NAME_COL])  
            _add_drug(drugs, row[SECOND_DRUG_NAME_COL])  
            _add_drug(drugs, row[THIRD_DRUG_NAME_COL])  
 
    for drug in drugs:
        storage.append(ent.Drug(drug))

def _add_drug(a_set, to_add):
    if to_add:
        a_set.add(to_add)

def make_ingredients(storage):
    with open(CSV_FILENAME, newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            _add_ingredient(storage, row, FIRST_DRUG_NAME_COL)  
            _add_ingredient(storage, row, SECOND_DRUG_NAME_COL)  
            _add_ingredient(storage, row, THIRD_DRUG_NAME_COL)  

def _add_ingredient(storage, row, drug_name_col):
    if row[drug_name_col]:
        ingredient_info = []

        for i in range(NUM_INGREDIENT_ATTR):
            ingredient_info.append(row[drug_name_col + i])

        storage.append(ent.Ingredient(ingredient_info))

if __name__ == "__main__":
    main()
