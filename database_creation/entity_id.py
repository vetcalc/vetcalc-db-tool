class EntityId:
    '''
    EntityIds will be represented as a prefix plus some number.
    This number can be whatever it needs to be, e.g., a sequence, UUID, or ULID.
    The prefix is their for debugging purposes to aid in quickly finding the
    table for search for a given id.
    '''

    def __init__(self, prefix: str, id: int):
        self.id = id
        self.prefix = prefix


    def __gt__(self, other):
        return self.get() > other.get()


    def __eq__(self, other):
        return self.get() == other.get()

    
    def __hash__(self):
        return hash((self.id, self.prefix))


    def get(self, no_prefix=False) -> int | str:
        if no_prefix:
            end_of_prefix = id.get().index("_")
            return int(id.get()[end_of_prefix+1:])
        else:
            return f"{self.prefix}_{self.id}"

    def set(self, id: int):
        self.id = id


def strip(id:str):
    end_of_prefix = id.index("_")
    return id[end_of_prefix+1:]
