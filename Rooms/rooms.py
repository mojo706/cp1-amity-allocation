class Room(object):
    """Class that expresses the attributes of each room. Office Space and LivingSpace
        inherit from this room.
    """

    def __init__(self, name):
        self.name = name
        self.occupants = []


class Office(Room):
    """This class defines an instance of each Office
    and inherits from Room class
    """

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
        self.room_type = "OFFICE"
        self.capacity = 6


class Living_Space(Room):
    """This class defines an instance of each Livingspace
    and inherits from Room class
    """

    def __init__(self, room_name):
        super(Living_Space, self).__init__(room_name)
        self.room_type = "LIVING SPACE"
        self.capacity = 4
