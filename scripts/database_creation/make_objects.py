import csv

import entities as ent

INPUT_CSV = "drugs.csv"

def make_entities():
    entities = dict()

    # Make entities by parsing csv
    entities["animals"] = make_objects_simple(ent.Animal, 1)
    entities["drugs"] = make_objects_simple(ent.Drug, 2)
    entities["units"] = make_units(ent.Unit)
    entities["methods"] = make_objects_with_delimiter(ent.Method, 3, ':')
    entities["dosages"] =  make_dosages(ent.Dosage, entities, ":")
    entities["concentrations"] = make_concentrations_from_entities(entities)
    
    return entities


def make_units(object_maker):
    concentration_units = make_objects_simple(object_maker, 5)
    dose_units = make_objects_simple(object_maker, 8)

    units = concentration_units + dose_units
    for unit in units:
        if unit.name == "":
            units.remove(unit)
    units = set_all_ids_consecutively(units)

    return units

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
            animal = search_objects_by_criterion(row[1], entities["animals"], "name")
            drug = search_objects_by_criterion(row[2], entities["drugs"], "name")
            if animal and drug:
                dosage = object_maker(animal.id, drug.id)
            else:
                continue
            
            methods = row[3].split(delimiter)
            for item in methods:
                method = search_objects_by_criterion(item, entities["methods"], "name")
                if method and dosage:
                    dosage.methods.add(method.id)
          
            concentration_number = force_as_none(row[4])
            concentration_unit = force_as_none(row[5])
            concentration = (concentration_number, concentration_unit)

            dose_low = force_as_none(row[6])
            dose_high = force_as_none(row[7])
            dose = (dose_low, dose_high)
            
            dose_unit = force_as_none(row[8])
            if dose_unit:
                dose_unit = search_objects_by_criterion(dose_unit, entities["units"], "name")
           
            if dose_unit is not None:
                dose_unit_id = dose_unit.id
            else:
                dose_unit_id = None

            notes = force_as_none(row[9])
           
            if dosage:
                dosage.concentration = concentration
                dosage.dose = dose
                dosage.dose_unit = dose_unit_id
                dosage.notes = notes

            dosages.append(dosage)
    
    dosages = set_all_ids_consecutively(dosages)

    return dosages


def make_concentrations_from_entities(entities):
    concentrations = []

    for dosage in entities["dosages"]:
        if dosage.concentration == (None, None):
            dosage.concentration = None
            continue
        value_string, unit_string = dosage.concentration
        
        unit = search_objects_by_criterion(unit_string, entities["units"], "name")
        if not unit:
            dosage.concentration = None
            continue

        if value_string:
            some_values = value_string.split(':')
        else:
            some_values = None

        if some_values:
            for value in some_values:
                concentration = ent.Concentration(float(value), unit.id, dosage.id)
                concentrations.append(concentration)
        else:
            concentration = ent.Concentration(None, unit.id, dosage.id)
            concentrations.append(concentration)
    
    concentrations = set_all_ids_consecutively(concentrations)

    return concentrations

def force_as_none(thing_to_force):
    if thing_to_force:
        return thing_to_force
    return None


def set_all_ids_consecutively(objects):
    for idx, object in enumerate(objects):
        object.id.set(idx+1)
    return objects


def search_objects_by_criterion(criterion, objects, attribute):
    for object in objects:
        if getattr(object, attribute) == criterion:
            return object
    return None

