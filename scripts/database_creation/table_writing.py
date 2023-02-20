DATABASE_IMPORT_PREFIX = "for_database_import"

def write_tables_as_csv(entities):
    _write_entities_into_csv(entities)
    _write_join_tables(entities)

def _write_entities_into_csv(entities):
    # convert the objects into rows in some csv files
    _write_objects_into_csv(entities["animals"],
                            "aniaml_id,name,temp_low,temp_high,heart_rate_low,heart_rate_high,respiratory_rate_low,respiratory_rate_high\n",
                            f'{DATABASE_IMPORT_PREFIX}/animals.csv'
                           )
    _write_objects_into_csv(entities["drugs"],
                            "drug_id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/drugs.csv'
                           )
    _write_objects_into_csv(entities["methods"],
                            "method_id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/methods.csv'
                           )
    _write_objects_into_csv(entities["concentrations"],
                            "concentration_id,value,unit_id,dosage_id\n",
                            f'{DATABASE_IMPORT_PREFIX}/concentrations.csv'
                           )
    _write_objects_into_csv(entities["units"],
                            "unit_id,name\n",
                            f'{DATABASE_IMPORT_PREFIX}/units.csv'
                           )
    _write_objects_into_csv(entities["dosages"], 
                            "dosage_id,animal_id,drug_id,dose_low,dose_high,dose_unit_id,notes\n",
                           f'{DATABASE_IMPORT_PREFIX}/dosages.csv'
                           )


def _write_objects_into_csv(storage, header, filename):
    with open(filename, 'w') as file:
        file.write(header) 
        for item in storage:
            file.write(item.format())


def _write_join_tables(entities):
    _join_dosages_methods(entities["dosages"],
                             "dosage_id,method_id\n",
                             f'{DATABASE_IMPORT_PREFIX}/dosages_join_methods.csv'
                             )

def _join_dosages_methods(storage, header, filename):
    with open(filename, 'w') as file:
        file.write(header) 

        for dosage in storage:
            for method in dosage.methods:
                file.write((f"{dosage.id.get()},"
                            f"{method.get()}\n"))

