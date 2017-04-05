class Person(object):
    """Class that expresses the attributes of each person. Fellow and Staff
        inherit from this room.
    """

    def __init__(self, person_id, name, designation, accomodated):
        self.uid = person_id
        self.name = name
        self.designation = designation
        self.accomodated = accomodated


class Fellow(Person):
    def __init__(self, person_id, name, designation, accomodated):
        super(Fellow, self).__init__(
            person_id, name, designation="FELLOW", accomodated="N")
        self.accomodated = accomodated


class Staff(Person):
    def __init__(self, person_id, name, designation, accomodated):
        super(Staff, self).__init__(
            person_id, name, designation="STAFF", accomodated="N")
