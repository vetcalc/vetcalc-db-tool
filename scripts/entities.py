class Drug:
    ''' 
    Purpose:
    
    Ingredients of combinations are made of drugs.
    This is the drug itself and revlevant information.

    Attributes:

    name           -- string
    '''

    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)


class Ingredient:
    '''
    Purpose:

    Contains the drug as used in a combination with contextual information
    
    Attributes:
    
    drug                    -- singular
    concentration           -- single number
    concentation_unit       -- string
    dosage                  -- as a tuple representing a range
    dosage_unit             -- string
    method                  -- how the ingredient is administered in the associated combinatino
    '''

    def __init__(self, info):
        self.drug = info[0]
        self.concentration = info[1]
        self.concenctration_unit = info[2] 
        self.dosage = info[3] 
        self.dosage_unit = info[4] 
        self.method = info[5] 

    def show(self):
        visual = (f"{self.drug} :\n"
                  f"\t{self.concentration} {self.concentration_unit}\n"
                  f"\t{self.dosage} {self.dosage_unit}\n"
                  f"\t{self.method}"
                 )
        print(visual)


class Combination:
    '''
    Purpose:

    Combinations of drugs are what animals need.
    Combinations use a number of ingredients with dosages.
    Instructions for administration are included here.

    Attributes:

    ingredients       -- as a list
    animal            -- singular
    for_juvenile      -- if the combination is for a juvenile animal
    combined_with     -- combintations containing a single drug can go with the specified drugs
    purpose           -- what this combination is used for
    notes             -- may include instructions for administration
    reference        -- where the info is found
    '''
    def __init__(self, animal, for_juvenile):
        self.animal = animal
        self.for_juvenile = for_juvenile
        self.ingredients = []
        self.combined_with = ""
        self.purpose = ""
        self.notes = ""
        self.reference = ""

    def add_ingredient(self, ingredient):
        self.ingredient.append(ingredient)

    def show(self):
        juvenile = "juvenile" if self.for_juvenile else ""
        visual = (f"Combo for {juvenile} {self.animal}\n"
                  f"\tGoes with {self.combined_with}\n"
                  f"\tContains: {self.ingredients}\n"
                  f"\tUsed for {self.purpose}\n"
                  f"\tNotes: {self.notes}\n"
                  f"\tFound in: {self.reference}\n"

                 )
        print(visual)


class Animal:
    '''
    Purpose:

    Is the type of animal being administered a drug.
    The physiological markers of health are also present.

    Attributes:

    name                -- string
    temperature         -- in celsius
    heart_rate          -- in beats per minute
    respiratory_rate    -- in breaths per minute
    '''
    def __init__(self, name):
        self.name = name
        self.temperature = 0 
        self.heart_rate = 0 
        self.respiratory_rate = 0 

    def show(self):
        visual = (f"{self.name} :\n"
                  f"\t{self.temperature} C \n"
                  f"\t{self.heart_rate} beats/min \n"
                  f"\t{self.respiratory_rate} breaths/min"
                 )
        print(visual)
