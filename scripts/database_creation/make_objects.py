import csv

import entities as ent

INPUT_CSV = "drugs.csv"

def make_entities():
    entities = dict()

    # Make entities by parsing csv
    entities["animals"] = make_objects_simple(ent.Animal, 1)
    entities["drugs"] = make_objects_simple(ent.Drug, 2)
    entities["methods"] = make_objects_with_delimiter(ent.Method, 3, ':')
    entities["dosages"] =  make_dosages(ent.Dosage, entities, ":")
      
    return entities


def make_objects_simple(object_maker, column_to_parse):
    names = set()
    objects = []

    with open(INPUT_CSV, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header
            names.add(row[column_to_parse])

    for name in sorted(names):
        objects.append(object_maker(name))

    objects = set_all_ids_consecutively(objects)

    return objects


def make_objects_with_delimiter(object_maker, column_to_parse, delimiter=None):
    names = set()
    objects = []

    with open(INPUT_CSV, newline='') as csv_file:
        reader = csv.reader(csv_file) 
        for idx, row in enumerate(reader):
            if idx == 0:
                continue # ignore the header

            names_present = row[column_to_parse].split(delimiter)
            [names.add(x) for x in names_present]

    for name in sorted(names):
        if name:
            objects.append(object_maker(name))

    # add on the ids
    objects = set_all_ids_consecutively(objects)

    return objects 


def make_dosages(object_maker, entities, delimiter):
    dosages = []

    with open(INPUT_CSV, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            
            dosage = None
            animal = search_objects_by_name(row[1], entities["animals"], "name")
            drug = search_objects_by_name(row[2], entities["drugs"], "name")
            if animal and drug:
                dosage = object_maker(animal.id, drug.id)
            
            methods = row[3].split(delimiter)
            for item in methods:
                method = search_objects_by_name(item, entities["methods"], "name")
                if method and dosage:
                    dosage.methods.add(method.id)
          
            concentration_number = force_as_none(row[4])
            concentration_unit = force_as_none(row[5])
            concentration = (concentration_number, concentration_unit)

            dose_low = force_as_none(row[6])
            dose_high = force_as_none(row[7])
            dose_unit = force_as_none(row[8])
            dose = (dose_low, dose_high, dose_unit)

            notes = force_as_none(row[9])
           
            if dosage:
                dosage.concentration = concentration
                dosage.dose = dose
                dosage.notes = notes

            dosages.append(dosage)
    
    dosages = set_all_ids_consecutively(dosages)

    return dosages


def force_as_none(thing_to_force):
    if thing_to_force:
        return thing_to_force
    return None


def set_all_ids_consecutively(objects):
    for idx, object in enumerate(objects):
        object.id.set(idx+1)
    return objects


def search_objects_by_name(criterion, objects, attribute):
    for object in objects:
        if getattr(object, attribute) == criterion:
            return object
    return None

