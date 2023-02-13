def remove_whitespace(item):
    try:
        item = "".join(item.split())
    except:
        pass
    finally:
        return item

def escape_characters(item):
    translation_table = {'"': r"\""}
    return item.translate(str.maketrans(translation_table))
