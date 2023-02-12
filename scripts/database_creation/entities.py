from entity_id import EntityId as eid

class Drug:
    ''' 
    Purpose:
    
    Ingredients of combinations are made of drugs.
    This is the drug itself and revlevant information.

    Attributes:

    id
    name           -- string
    '''
    def __init__(self, name):
        self.id = eid("d", 0)
        self.name = name

    def show(self):
        visual = (f"{self.id.get()}: \n"
                  f"\t{self.name}"
                 )
        print(visual)
    
    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name}\n"
              )
        return row


class Ingredient:
    '''
    Purpose:

    Contains the drug as used in a combination with contextual information
    
    Attributes:
   
    id
    combination             -- as a singular id
    drug                    -- as a singular id
    concentration           -- single number
    concentation_unit       -- string
    dosage                  -- as a tuple representing a range
    dosage_unit             -- string
    methods                  -- as a list of ids
    '''

    def __init__(self, info):
        self.id = eid("i", 0)
        self.combination = ""
        self.drug = info[0]
        self.concentration = info[1]
        self.concentration_unit = info[2] 
        self.dosage = info[3] 
        self.dosage_unit = info[4] 
        self.methods = info[5] 

    def show(self):
        visual = (f"{self.id.get()} :\n"
                  f"\t{self.drug}\n"
                  f"\t{self.concentration} {self.concentration_unit}\n"
                  f"\t{self.dosage} {self.dosage_unit}\n"
                  f"\t{self.methods}"
                 )
        print(visual)

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.combination},"
               f"{self.drug},"
               f"{self.concentration},"
               f"{self.concentration_unit},"
               f"{self.dosage},"
               f"{self.dosage_unit}\n"
              )

        return row

    def matches(self, info):
        if not info:
            return False
        if info[0] != self.drug:
            return False
        if info[1] != self.concentration:
            return False
        if info[2] != self.concentration_unit:
            return False
        if info[3] != self.dosage:
            return False
        if info[4] != self.dosage_unit:
            return False
        if info[5] != self.methods:
            return False
        return True

class Combination:
    '''
    Purpose:

    Combinations of drugs are what animals need.
    Combinations use a number of ingredients with dosages.
    Instructions for administration are included here.

    Attributes:

    id
    ingredients       -- as a list of list of ingredients
    animal            -- a singular id
    for_juvenile      -- if the combination is for a juvenile animal
    combined_with     -- combintations containing a single drug can go with the specified drugs
    purpose           -- what this combination is used for
    notes             -- may include instructions for administration
    reference        -- where the info is found
    '''
    def __init__(self, animal, for_juvenile):
        self.id = eid("c", 0)
        self.animal = animal
        self.for_juvenile = for_juvenile
        self.ingredients = []
        self.combined_with = ""
        self.purpose = ""
        self.notes = ""
        self.reference = ""

    def add_ingredients(self, ingredients):
        self.ingredients.append(ingredients)

    def show(self):
        juvenile = "juvenile" if self.for_juvenile else ""
        visual = (f"Combo {self.id.get()} for {juvenile} {self.animal}\n"
                  f"\tGoes with {self.combined_with}\n"
                  f"\tContains: {self.ingredients}\n"
                  f"\tUsed for {self.purpose}\n"
                  f"\tNotes: {self.notes}\n"
                  f"\tFound in: {self.reference}\n"

                 )
        print(visual)

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.animal},"
               f"{self.for_juvenile},"
               f"{self.purpose},"
               f"{self.notes},"
               f"{self.reference}\n"
              )
        return row
 

class Animal:
    '''
    Purpose:

    Is the type of animal being administered a drug.
    The physiological markers of health are also present.

    Attributes:

    id
    name                -- string
    temperature         -- in celsius
    heart_rate          -- in beats per minute
    respiratory_rate    -- in breaths per minute
    '''
    def __init__(self, name):
        self.id = eid("a", 0)
        self.name = name
        self.temperature = 0 
        self.heart_rate = 0 
        self.respiratory_rate = 0 

    def show(self):
        visual = (f"{self.id.get()} :\n"
                  f"\t{self.name}\n"
                  f"\t{self.temperature} C \n"
                  f"\t{self.heart_rate} beats/min \n"
                  f"\t{self.respiratory_rate} breaths/min"
                 )
        print(visual)

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name},"
               f"{self.temperature},"
               f"{self.heart_rate},"
               f"{self.respiratory_rate}\n"
              )
        return row
 

class Method:
    '''
    Purpose:

    Contains the different ways ingredients can be administered

    Attributes:

    id
    name        -- string

    '''
    def __init__(self, name):
        self.id = eid("m", 0)
        self.name = name

    def show(self):
        visual = (f"{self.id.get()} :\n"
                  f"\t{self.name}"
                 )
        print(visual)

    def format(self):
        row = (f"{self.id.get()},"
               f"{self.name}\n"
              )
        return row
