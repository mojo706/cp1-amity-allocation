from Rooms.rooms import Room, Office, Living_Space
from Persons.persons import Person, Fellow, Staff
from random import randint
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
        self.all_people = self.fellows + self.staff

    def create_room(self, room_type, room_name):
        """Create a new room, a room can either be an office or living_space,
        then check to make sure no room with the same name exits
         before successfully creating the room
        """

        if not isinstance(room_name, str) or not isinstance(room_type, str):
            raise ValueError("Invalid Input")

        if room_name in self.all_rooms:
            msg = "The room {} has already been created".format(room_name)
            print(msg)
            return msg

        if room_type.upper() == "OFFICE":
            newOffice = Office(room_name)
            self.offices.append(newOffice)
            self.all_rooms.append(room_name)
            msg = "Office Successfully Created"
            print(msg)

        if room_type.upper() == "LIVINGSPACE":
            newLivingSpace = Living_Space(room_name)
            self.living_spaces.append(newLivingSpace)
            self.all_rooms.append(room_name)
            msg = "Living Space Successfully Created"
            print(msg)


    def randomized_allocation(self):
        """ Allocate a person an office or living space"""
        random.choice()

    def add_person(self, name, role, accomodated="N"):
        """ Add person to Amity and assign them an office space or
        living space"""
        person_id = randint(1000, 9999)

        if not name.isalpha() and not role.isalpha():
            raise ValueError("Invalid Input")

        if role.upper() == "STAFF":
            if name in self.all_people:
                print("That Staff member already exists")
            newStaff = Staff(person_id, name)
            self.staff.append(newStaff)
            msg = "The person {} has been successfully added".format(name)
            print(msg)
            return msg

        elif role.upper() == "FELLOW":
            if name in self.staff:
                print("That Fellow already exists")
            newFellow = Fellow(person_id, name)
            self.fellows.append(newFellow)
            msg = "The person {} has been successfully added".format(name)
            print(msg)
            return msg

    def allocate_unallocated(self):
        """ used to allocate fellows or staff who were previously
        unallocated """

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
