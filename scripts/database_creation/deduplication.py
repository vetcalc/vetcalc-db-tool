import string_manipulation as sm
from operator import attrgetter

def dedup_entities(entities):
    '''
    denormalizes entities for sql tables
    '''
    entities["combinations"] = _dedup_combinations(entities["combinations"])
    entities["ingredients"] = _gather_ingredients(entities["combinations"])
    entities["ingredients"] = _dedup_ingredients(entities["ingredients"])

def _gather_ingredients(combinations):
    ingredients = []

    for combo in combinations:
        for a_list in combo.ingredients:
            for ingredient in a_list:
                ingredient.combination = combo.id.get()
                ingredients.append(ingredient)

    # convert methods from a string to a collection
    for ingredient in ingredients:
        method = ingredient.methods
        ingredient.methods = set()
        ingredient.methods.add(method)

    return ingredients


def _dedup_ingredients(ingredients):
    '''
    combine similar ingredients together 
    '''
    normalized = []

    for ingredient in ingredients:
        _add_to_normalized_ingredients(ingredient, normalized)

    sorted_items = sorted(normalized, key=attrgetter("combination", "drug"))

    return sorted_items


def _add_to_normalized_ingredients(ingredient, normalized):
    match_idx = _contains_ingredient(ingredient, normalized)
    if match_idx == -1:
        normalized.append(ingredient)
    else:
        for method in ingredient.methods:
            normalized[match_idx].methods.add(method)


def _contains_ingredient(ingredient, a_list):
    if not a_list:
        return -1
    
    for idx, an_ingredient in enumerate(a_list):
        if _ingredients_match(ingredient, an_ingredient):
            return idx

    return -1


def _ingredients_match(first, second):
    if first.combination != second.combination:
        return False
    if first.drug != second.drug:
        return False
    if sm.remove_whitespace(first.concentration) != sm.remove_whitespace(second.concentration):
        return False
    if sm.remove_whitespace(first.concentration_unit) != sm.remove_whitespace(second.concentration_unit):
        return False
    if sm.remove_whitespace(first.dosage) != sm.remove_whitespace(second.dosage):
        return False
    if sm.remove_whitespace(first.dosage_unit) != sm.remove_whitespace(second.dosage_unit):
        return False
    return True


def _dedup_combinations(combinations):
    '''
    Look through combinations and combine similar combinations
    by filtering into a second list
    '''
    normalized = []

    for combination in combinations:
        _add_to_normalized_combinations(combination, normalized)

    for idx, combination in enumerate(normalized):
        combination.id.set(idx+1)

    return normalized

def _add_to_normalized_combinations(combination, normalized):
    match_idx = _contains_combination(combination, normalized)
    if match_idx == -1:
        normalized.append(combination)
    else:        
        for ingredient_list in combination.ingredients:
            normalized[match_idx].ingredients.append(ingredient_list)


def _contains_combination(combination, a_list):
    if not a_list:
        return -1
    
    for idx, a_combo in enumerate(a_list):
        if _combinations_match(combination, a_combo):
            return idx

    return -1
   

def _combinations_match(combo_1, combo_2):
    if combo_1.animal != combo_2.animal:
        return False
    if combo_1.for_juvenile != combo_2.for_juvenile:
        return False
    if sm.remove_whitespace(combo_1.combined_with) != sm.remove_whitespace(combo_2.combined_with):
        return False
    if sm.remove_whitespace(combo_1.purpose) != sm.remove_whitespace(combo_2.purpose):
        return False
    if sm.remove_whitespace(combo_1.notes) != sm.remove_whitespace(combo_2.notes):
        return False
    if sm.remove_whitespace(combo_1.reference) != sm.remove_whitespace(combo_2.reference):
        return False
    if not _ingredient_lists_match(combo_1.ingredients, combo_2.ingredients):
        return False
    return True


def _ingredient_lists_match(list_1, list_2):
    # there must be the same number of ingredients
    if len(list_1[0]) != len(list_2[0]):
        return False

    # and the names must match
    names = set()
    for ingredient in list_1[0]:
        names.add(ingredient.drug)

    for ingredient in list_2[0]:
        if ingredient.drug not in names:
            return False

    return True

