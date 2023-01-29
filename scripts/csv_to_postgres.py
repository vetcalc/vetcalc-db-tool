import csv
import entities as ent

CSV_FILENAME = "drugs.csv"
NUM_DRUG_ATTR = 6
FIRST_DRUG_NAME_COL = 3

g_animals = []
g_drugs = []
g_ingredients = []
g_combinations = []

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
            _add_drug(drugs, row[FIRST_DRUG_NAME_COL + NUM_DRUG_ATTR]) 
            _add_drug(drugs, row[FIRST_DRUG_NAME_COL + 2 * NUM_DRUG_ATTR]) 
 
    for drug in drugs:
        storage.append(ent.Drug(drug))

def _add_drug(a_set, to_add):
    if to_add:
        a_set.add(to_add)

def make_ingredients(storage):
    pass

def make_combinations(storage):
    pass

def parse_row(row):
    column = 0

    animal = ent.Animal(row[column])
    column += 1

    for_juvenile = row[column]
    column += 1
   
    combination = ent.Combination(animal.name, for_juvenile)

    combination.combined_with = row[column+1]
    column += 1

    for j in range(3):
        temp_ingredient = []

        for i in range(6):
            temp_ingredient.append(row[column])
            column += 1

        drug = ent.Drug(temp_ingredient[0])
        ingredient = ent.Ingredient(temp_ingredient)

    combination.purpose = row[column]
    column += 1

    combination.notes = row[column]
    column += 1

    combination.reference = row[column]
    column += 1

if __name__ == "__main__":
    main()
