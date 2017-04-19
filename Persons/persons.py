class Person(object):
    """Class that expresses the attributes of each person. Fellow and Staff
        inherit from this room.
    """

    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name


class Fellow(Person):
    """ Fellow Class that defines a fellow"""
    def __init__(self, person_id, name):
        super(Fellow, self).__init__(person_id, name)
        self.accomodated = None
        self.allocated = None


class Staff(Person):
    """ Staff Class that defines a staff"""
    def __init__(self, person_id, name):
        super(Staff, self).__init__(person_id, name)
        self.allocated = None
