from Rooms.rooms import Room

""" This file contains all the functions of the amity cli app """


class Amity(object):
    """ Main Class for all the methods the other classes to inherit from """

    def __init__(self):
        self.offices = []
        self.living_spaces = []
        self.fellows = []
        self.staff = []
        self.waiting_list = []
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, room_name):
        """Create a new room, a room can either be an office or living_space,
        then check to make sure no room with the same name exits
         before successfully creating the room
        """

        if not isinstance(room_name, str) or not isinstance(room_type, str):
            raise ValueError("Invalid Input")

        if room_name.upper() in [room.room_name for room in self.all_rooms]:
            print(" The room % s has already been created)
        if room_type.upper() == "OFFICE":
            newOffice = Office(room_name)
            self.offices.append(room_name)
            self.all_rooms.append(room_name)
            msg = "Office Successfully Created"
            print(msg)

        elif room_type.upper() == "LIVINGSPACE":
            newLivingSpace = Living_Space(room_name)
            self.living_spaces.append(room_name)
            self.all_rooms.append(room_name)
            msg = "Living Space Successfully Created"
            print(msg)

    def allocate_person_to_room(self):
        """ Allocate a person an office or living space"""
        pass

    def add_person(self, first_name, last_name, email, role, accomodated="N"):
        """ Add person to Amity and assign them an office space or
        living space"""

    def reallocate_person(self):
        """ Move a person from one office space or living space to another"""
        pass

    def print_allocations(self):
        """ Print people and the rooms they have been allocated """
        pass

    def save_allocations_to_file(self):
        """ Save people and the rooms they have been allocated to file"""
        pass

    def print_unallocated(self):
        """ Print a list of people who have not been allocated a room"""
        pass
