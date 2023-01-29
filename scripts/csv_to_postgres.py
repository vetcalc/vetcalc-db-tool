import csv
import entities as ent

animals = []

def main():
    
    with open('drugs.csv', newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='|')
        
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            print(row)
           
            if idx > 4:
                break

if __name__ == "__main__":
    main()
