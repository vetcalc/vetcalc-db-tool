from entity_id import EntityId as eid

class Drug:
    ''' 
    Purpose:
        dosages are made of drugs
    '''
    def __init__(self, name: str):
        self.id = eid("dr", 0)
        self.name = name

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name}\n"
               )
        return row

class Dosage:
    '''
    Purpose:
        dosages are made of drugs and are given to an animal using a method
    '''

    def __init__(self, animal: eid, drug: eid):
        self.id = eid("do", 0)
        self.animal = animal
        self.drug = drug
        self.methods: set[eid] = set()
        self.concentration: tuple[float, str] = tuple()
        self.dose: tuple[float, float] = tuple()
        self.dose_unit: eid | None = None
        self.notes = ""


    def format(self):
        if self.dose_unit:
            dose_unit = self.dose_unit.get()
        else:
            dose_unit = None

        row = (f"{self.id.get()},"
               f"{self.animal.get()},"
               f"{self.drug.get()},"
               f"{self.dose[0]},"
               f"{self.dose[1]},"
               f"{dose_unit},"
               f"{self.notes}\n"
              )
        return row


class Animal:
    '''
    Purpose:
        Is the type of animal being administered a drug.
        The physiological markers of health are also present.

    Attributes:
        temperature         -- in celsius
        heart_rate          -- in beats per minute
        respiratory_rate    -- in breaths per minute
    '''
    def __init__(self, name: str):
        self.id = eid("a", 0)
        self.name = name
        self.temperature = (0, 0)
        self.heart_rate = (0, 0) 
        self.respiratory_rate = (0, 0) 

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name},"
               f"{self.temperature[0]},"
               f"{self.temperature[1]},"
               f"{self.heart_rate[0]},"
               f"{self.heart_rate[1]},"
               f"{self.respiratory_rate[0]},"
               f"{self.respiratory_rate[1]}\n"
              )
        return row


class Method:
    '''
    Purpose:
        Contains the different ways drugs can be administered
    '''
    def __init__(self, name: str):
        self.id = eid("m", 0)
        self.name = name

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name}\n"
              )
        return row


class Concentration:
    '''
    Purpose:
        allows for dosages to have multiple concentrations
    '''
    def __init__(self, value: float | None, unit_id: eid, dosage_id: eid):
        self.id = eid("c", 0)
        self.value = value
        self.unit_id = unit_id
        self.dosage_id = dosage_id

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.value},"
               f"{self.unit_id.get()},"
               f"{self.dosage_id.get()}\n"
              )
        return row

class Unit:
    '''
    Purpose:
        Contains strings of possible units
    '''
    def __init__(self, name: str):
        self.id = eid("u", 0)
        self.name = name

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name}\n"
              )
        return row
