import csv
import entities as ent

g_animals = []

def main():
   
    make_animals(g_animals) 
    for animal in g_animals:
        print(animal.name)
    
    with open('drugs.csv', newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|')
        
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            if idx > 1:
                break
            # parse_row(row)
            print(row)
   
def make_animals(storage):
    names = set()

    with open('drugs.csv', newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|') 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            names.add(row[0])

    for name in names:
        storage.append(ent.Animal(name))

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
