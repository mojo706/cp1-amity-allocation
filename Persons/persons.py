class Person(object):
    """Class that expresses the attributes of each person. Fellow and Staff
        inherit from this room.
    """

    def __init__(self, person_id, name):
        self.uid = person_id
        self.name = name


class Fellow(Person):
    def __init__(self, person_id, name, role, wants_accomodation):
        super(Fellow, self).__init__(person_id, name)
        self.allocated = False


class Staff(Person):
    def __init__(self, person_id, name, role, wants_accomodation):
        super(Staff, self).__init__(person_id, name)
        self.allocated = False
