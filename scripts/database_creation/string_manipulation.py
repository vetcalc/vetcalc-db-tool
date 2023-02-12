def remove_whitespace(item):
    try:
        item = "".join(item.split())
    except:
        pass
    finally:
        return item

