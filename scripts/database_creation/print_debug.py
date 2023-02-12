

def show_entities(entities):
    # Pretty print the results
    # _show_items(entities["animals"], "Animals:")
    # _show_items(entities["drugs"], "Drugs:")
    # _show_items(entities["methods"], "Methods:")
    # _show_items(entities["ingredients"], "Ingredients:")
    # _show_items(entities["combinations"], "Combinations:")
    # _show_detailed_combinations(entities["combinations"])

    return


def _show_detailed_combinations(combinations):
    for combo in combinations:
        combo.show()
        for idx, ingredient_list in enumerate(combo.ingredients):
            print(f"List {idx}")
            [ingredient.show() for ingredient in ingredient_list]
    return 

def _show_items(storage, title):
    print(title)
    for item in storage:
        item.show()

