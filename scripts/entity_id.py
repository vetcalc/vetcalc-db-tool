class EntityId:
    '''
    EntityIds will be represented as a prefix plus some number.
    This number can be whatever it needs to be, e.g., a sequence, UUID, or ULID.
    The prefix is their for debugging purposes to aid in quickly finding the
    table for search for a given entity.
    '''

    def __init__(self, prefix, id):
        self.id = id
        self.prefix = prefix

    def show(self):
        print (f"{self.prefix}_{self.id}")

    def get(self):
        return f"{self.prefix}_{self.id}"

    def set(self, id):
        self.id = id

    def is_set(self):
        if self.id != 0:
            return True
        else:
            return False
