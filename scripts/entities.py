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

    def __init__(self, drug, concentration, concentration_unit, dosage, dosage_unit, method):
        self.drug = drug
        self.concentration = concentration
        self.concenctration_unit = concentration_unit
        self.dosage = dosage
        self.dosage_unit = dosage_unit
        self.method = method

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
        self.reference == ""

    def add_ingredient(self, ingredient):
        self.ingredient.append(ingredient)

class Animal:
    '''
    Purpose:

    Is the type of animal being administered a drug.
    The physiological markers of health are also present.

    Attributes:

    name                -- string
    temperature         -- in celsius
    heart_rate          -- in bpm
    respiratory_rate    -- in ???
    '''
    def __init__(self, name, temperature, heart_rate, respiratory_rate):
        self.name = name
        self.temperature = temperature
        self.heart_rate = heart_rate
        self.respiratory_rate = respiratory_rate
