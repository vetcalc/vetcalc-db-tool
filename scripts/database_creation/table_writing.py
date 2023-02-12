DATABASE_IMPORT_PREFIX = "for_database_import"

def write_tables_as_csv(entities):
    _write_entities_into_csv(entities)
    _write_join_tables(entities)

def _write_entities_into_csv(entities):
    # convert the objects into rows in some csv files
    _write_objects_into_csv(entities["animals"],
                            "id,name,temperature,heart_rate,respiratory_rate\n",
                            f'{DATABASE_IMPORT_PREFIX}/animals.csv'
                           )
    _write_objects_into_csv(entities["drugs"],
                            "id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/drugs.csv'
                           )
    _write_objects_into_csv(entities["methods"],
                            "id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/methods.csv'
                           )
    _write_objects_into_csv(entities["ingredients"],
                            "id,combination,drug,concentration,concentration_unit,dosage,dosage_unit\n",
                            f'{DATABASE_IMPORT_PREFIX}/ingredients.csv'
                           )
    _write_objects_into_csv(entities["combinations"], 
                            "id,animal,for_juvenile,combined_with,purpose,notes,reference\n",
                           f'{DATABASE_IMPORT_PREFIX}/combinations.csv'
                           )


def _write_objects_into_csv(storage, header, filename):
    with open(filename, 'w') as file:
        file.write(header) 
        for item in storage:
            file.write(item.format())


def _write_join_tables(entities):
    _join_ingredients_methods(entities["ingredients"],
                             "ingredient_id,method_id\n",
                             f'{DATABASE_IMPORT_PREFIX}/ingredients_join_methods.csv'
                             )

def _join_ingredients_methods(storage, header, filename):
    with open(filename, 'w') as file:
        file.write(header) 

        for ingredient in storage:
            for method in ingredient.methods:
                if method:
                    file.write(f"{ingredient.id.get()},{method}\n")


