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
        self.office_waitlist = []
        self.living_waitlist = []
        self.all_rooms = []
        self.person_status = False

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
            new_office = Office(room_name)
            self.offices.append(new_office)
            self.all_rooms.append(room_name)
            msg = "Office Successfully Created"
            print(msg)
            return msg

        if room_type.upper() == "LIVINGSPACE":
            new_living_space = Living_Space(room_name)
            self.living_spaces.append(new_living_space)
            self.all_rooms.append(room_name)
            msg = "Living Space Successfully Created"
            print(msg)
            return msg

    def add_person(self, name, role, accomodated="N"):
        """ Add person to Amity and assign them an office space or
        living space"""
        person_id = randint(1000, 9999)
        roles = ["STAFF", "FELLOW"]
        role = role.upper()
        office_allocation = allocate_office_space()

        if not isinstance(name, str) and not isinstance(role, str):
            raise ValueError(" Name and Role must be string")

        if role not in roles:
            raise ValueError("Invalid Role")

        if role == "STAFF":
            if name in self.staff:
                msg = "That Staff member already exists"
                print(msg)
                return msg
            new_staff = Staff(person_id, name, role, accomodated)
            self.staff.append(new_staff)
            msg = "The staff member {} has been successfully added".format(
                name)
            print(msg)
            print(self.allocate_office_space(new_staff))

        elif role == "FELLOW":
            if name in self.fellows:
                msg = "That Fellow already exists"
                print(msg)
                return msg
            new_fellow = Fellow(person_id, name, role, accomodated)
            self.fellows.append(new_fellow)
            msg = "The fellow {} has been successfully added".format(name)
            print(msg)
            print(self.allocate_office_space(new_fellow))

    def allocate_office_space(self, person):
        """ A method that randomly allocates an available office to a fellow or
         member of staff """
        available_offices = []

        # loop through all the offices and determine all available offices
        for office in self.offices:
            if len(office.occupants) < office.capacity:
                available_offices.append(office)

        if available_offices:
            allocated_room = random.choice(available_offices)
            allocated_room.occupants.append(person)
            person.office = allocated_room.name
            self.person_status = True
            msg = "{} has been allocated the livingspace {} ".format(
                person.name, allocated_room.name)
            return msg
        else:
            print("No available offices")
            self.office_waitlist.append(person)
            return "{} has been added to the office waiting list".format(
                person.name)

    def allocate_living_space(self, person):
        """ A method that randomly allocates an available living space to a
         fellow """
        available_livingspace = []
        # loop through all the living spaces and determine all available living
        # spaces
        for living_space in self.all_livingspace:
            if len(living_space.occupants) < living_space.capacity:
                available.append(living_space)

        if available_livingspace:
            allocated_room = random.choice(available_livingspace)
            allocated_room.occupants.append(person)
            person.livingspace = allocated_room.name
            self.person_status = True
            msg = "{} has been allocated the livingspace {}".format(
                person.name, allocated_room.name)
            return msg
        else:
            print("No available Living Spaces")
            self.living_waitlist.append(person)
            return "{} has been added to the Living Space waiting list".format(
                person.name)

    def print_room(self, room_name):
        """ Prints the names of all the people in room_name on the
             screen """
        if room_name not in self.all_rooms:
            msg = " The room {} doesn't exist ".format(room_name)
        else:
            if room_name in self.offices:
                for person in self.offices(room_name):
                    print(person)
            elif room_name in self.living_spaces:
                for person in self.living_spaces(room_name):
                    print(person)

    def allocate_unallocated(self, room_name):
        """ used to allocate fellows or staff who were previously
        unallocated """
        allocations = []
        if room_type.upper() == "LIVINGSPACE":
            for person in self.living_waitlist:
                print(self.allocate_living_space(person))
                if self.person_status:
                    allocations.append(person)
        # Update living space waiting list
        new_living_waitlist = list(
            set(self.living_waitlist) - set(allocations))
        self.living_waitlist = new_living_waitlist

        if room_type.upper() == "OFFICE":
            for person in self.office_waitlist:
                print(self.allocate_office_space(person))
                if self.person_status:
                    allocations.append(person)
        # Update office waiting list
        new_office_waitlist = list(
            set(self.office_waitlist) - set(allocations))
        self.office_waitlist = new_office_waitlist

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
