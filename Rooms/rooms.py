class Room(object):
    """Class that expresses the attributes of each room. Office Space and LivingSpace
        inherit from this room.
    """

    def __init__(self, name):
        self.name = name
        self.occupants = []


class OfficeSpace(Room):
    """This class defines an instance of each Office
    and inherits from Room class
    """

    def __init__(self, room_name):
        super(OfficeSpace, self).__init__(room_name)
        self.room_type = "OFFICE"
        self.capacity = 6


class LivingSpace(Room):
    """This class defines an instance of each Livingspace
    and inherits from Room class
    """

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)
        self.room_type = "LIVING SPACE"
        self.capacity = 4
