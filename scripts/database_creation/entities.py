from entity_id import EntityId as eid

class Drug:
    ''' 
    Purpose:
        dosages are made of drugs
    '''
    def __init__(self, name: str):
        self.id = eid("dr", 0)
        self.name = name


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
        self.concentration: tuple[int, str] = tuple()
        self.dose: tuple[int, int, str] = tuple()
        self.notes = ""


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


class Method:
    '''
    Purpose:
        Contains the different ways drugs can be administered
    '''
    def __init__(self, name: str):
        self.id = eid("m", 0)
        self.name = name

