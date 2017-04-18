import os
import random
import itertools

from Persons.persons import Person, Fellow, Staff
from Rooms.rooms import Room, Office, Living_Space

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

    def create_room(self, room_type, *room_names):
        """Create a new room, a room can either be an office or living_space,
        then check to make sure no room with the same name exits
         before successfully creating the room
        """

        for room_name in room_names[0]:
            if not isinstance(room_name, str) or not isinstance(room_type, str):
                raise ValueError("Invalid Input")

            if room_name in self.all_rooms:
                msg = "The room {} has already been created".format(room_name)
                print(msg)
                return msg

            if room_type.upper() == "OFFICE":
                new_office = Office(room_name)
                self.offices.append(new_office)
                self.all_rooms.append(room_name.upper())
                msg = "Office Successfully Created"
                print(msg)
                return msg

            if room_type.upper() == "LIVINGSPACE":
                new_living_space = Living_Space(room_name)
                self.living_spaces.append(new_living_space)
                self.all_rooms.append(room_name.upper())
                msg = "Living Space Successfully Created"
                print(msg)
                return msg

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
            msg = "{} has been allocated the office {}".format(
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
        for living_space in self.living_spaces:
            if len(living_space.occupants) < living_space.capacity:
                available_livingspace.append(living_space)

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

    def add_person(self, name, role, wants_accomodation="N"):
        """ Add person to Amity and assign them an office space or
        living space"""
        person_id = random.randint(1000, 9999)
        roles = ["STAFF", "FELLOW"]
        role = role.upper()
        name = name.upper()
        # import pdb
        # pdb.set_trace()
        if not isinstance(name, str) and not isinstance(role, str):
            raise ValueError(" Name and Role must be string")

        if role not in roles:
            raise ValueError("Invalid Role")

        if role == "STAFF":
            if name in self.staff:
                msg = "That Staff member already exists"
                print(msg)
                return msg
            new_staff = Staff(person_id, name, role, wants_accomodation)
            self.staff.append(new_staff)
            msg = "The staff member {} has been successfully added and ".format(
                name)
            allocation_msg = self.allocate_office_space(new_staff)
            success_msg = msg + allocation_msg
            print(success_msg)
            return success_msg

        elif role == "FELLOW":
            if name in self.fellows:
                msg = "That Fellow already exists"
                print(msg)
                return msg
            new_fellow = Fellow(person_id, name, role, wants_accomodation)
            self.fellows.append(new_fellow)
            msg = "The fellow {} has been successfully added and ".format(name)
            allocation_msg = self.allocate_office_space(new_fellow)

            success_msg = msg + allocation_msg
            print(success_msg)
            return success_msg

    # def print_room(self, room_name):
    #     """ Prints the names of all the people in room_name on the
    #          screen """
    #     if room_name not in self.all_rooms:
    #         msg = " The room {} doesn't exist ".format(room_name)
    #     else:
    #         if room_name in self.offices:
    #             for person in self.offices(room_name):
    #                 print(person)
    #         elif room_name in self.living_spaces:
    #             for person in self.living_spaces(room_name):
    #                 print(person)

    def allocate_unallocated(self, room_type, room_name):
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

    def reallocate_person(self, person_id, r_room):
        """This method reallocates a person using their unique identifier,
        in this case their email address, to a the specified new room
        """

        try:
            reallocated_person = [member for member in itertools.chain(self.staff, self.fellows)
                                  if member.person_id == person_id][0]
        except IndexError:
            return "Could not find person with the ID {}!".format(person_id)
        try:
            new_room = [room for room in itertools.chain(self.offices, self.living_spaces)
                        if room.name == r_room][0]
        except IndexError:
            return ("The room {} does not exist!") .format(r_room)

        if new_room.room_type == "LIVING SPACE":
            if reallocated_person.role == "STAFF":
                return "Cannot reallocate STAFF to LIVING SPACE!"

            if reallocated_person.wants_accomodation != "Y":
                return "Cannot reallocate! This FELLOW does not require LIVING SPACE!"
            if len(new_room.occupants) == 4:
                return "The room {} is full! Can not reallocate {}-{}!".format(r_room, reallocated_person.role, reallocated_person.name)

        if r_room.room_type == "OFFICE" and len(new_room.occupants) == 6:
            return "The room {} is full! Cannot reallocate {}-{}!".format(r_room, reallocated_person.role, reallocated_person.name)

        for room in itertools.chain(self.offices, self.living_spaces):
            for occupant in room.occupants:
                if occupant == reallocated_person:
                    current_room = room

        if current_room == r_room:
            return "Cannot reallocate to the same {}".format(current_room.room_type)
        else:
            current_room.occupants.remove(reallocated_person)
            r_room.occupants.append(reallocated_person)

            return "{}-{} was succesfully reallocated to {} {}".format(reallocated_person.role,
                                                                       reallocated_person.name,
                                                                       r_room.room_type,
                                                                       r_room.name)

    # def reallocate_person(self, person_name, r_room):
    #     """ Move a person from one office or living space to another """
    #     person_name = person_name.upper()

    #     available_livingspace = [living_space.name.upper() for living_space in self.living_spaces if len(
    #         living_space.occupants) < living_space.capacity]
    #     available_offices = [office.name.upper() for office in self.offices if len(
    #         office.occupants) < office.capacity]

    #     # Check if the person exists

    #     fellow_names = [fellow.person_name.upper() for fellow in self.fellows]
    #     staff_names = [staff_details.person_name.upper()
    #                    for staff_details in self.staff]

    #     if person_name not in fellow_names and person_name not in staff_names:
    #         msg = "The person {} does not exist".format(person_name)
    #         print(msg)
    #         return msg

    #     elif r_room.upper() not in available_offices and r_room.upper(
    #     ) not in available_livingspace:
    #         msg = " The room {} does not exist or isn't available ".format(
    #             r_room)
    #         print(msg)
    #         return msg
    #     else:

    # if r_room.upper() in available_offices and r_room.upper() not in
    # available_livingspace:

    #             current_office_index = []
    #             occupant_index = []
    #             for index in range(len(self.offices)):
    #                 for person_index in range(len(self.offices[index].occupants)):
    #                     print(
    #                         '\nWE ARE HERE', self.offices[index].occupants[person_index].person_name)
    #                     if person_name == self.offices[index].occupants[person_index].person_name:
    #                         occupant_index.append(person_index)
    #                         current_office_index.append(index)

    #             new_office_index = [index for index in range(
    # len(self.offices)) if self.offices[index].room_name == r_room]

    #             if current_office_index and occupant_index:
    #                 current_office_index = current_office_index[0]
    #                 occupant_index = occupant_index[0]

    #                 if new_office_index:
    #                     new_office_index = new_office_index[0]

    #                 del self.offices[current_office_index].occupants[occupant_index]
    #                 self.offices[new_office_index].occupants.append(
    #                     person_name)

    #                 # for room in self.offices:
    #                 #     if person_name in room.occupants:
    #                 #         c_offices = room.name
    #                 #         c_offices.remove(person_name)
    #                 #         new_office.occupants.append(person_name)
    #                 #         msg = "{} successfully reallocated to {}".format(
    #                 #             person_name, new_office)
    #                 #         print(msg)
    #                 #         return msg
    #                 msg = "{} successfully reallocated to {}".format(
    #                     person_name, self.offices[new_office_index].room_name)
    #                 print(msg)
    #                 return msg
    #             else:
    #                 msg = "The room {} has to be an office"
    #                 print(msg)
    #                 return msg

    #         elif r_room.upper() in available_livingspace and r_room.upper() not in available_offices:
    #             if person_name in fellow_names:

    #                 new_livingspace = [
    #                     room_details.room_name for room_details in self.living_spaces if room_details.room_name == r_room]
    #                 if new_livingspace:
    #                     for room in self.living_spaces:
    #                         if person_name in room.occupants:
    #                             c_livingspace = room.room_name
    #                             c_livingspace.remove(person_name)
    #                             new_livingspace.occupants.append(person_name)
    #                             msg = "{} successfully reallocated to {}".format(
    #                                 person_name, new_livingspace)
    #                             print(msg)
    #                             return msg
    #                 else:
    #                     msg = "The room {} has to be an living space"
    #                     print(msg)
    #                     return msg
    #         else:
    #             msg = "Neither an office nor a living space"
    #             print(msg)
    #             return msg

    # def reallocate_person(self, person_name, r_room):
    #     person_name = person_name.upper()
    #     """ Move a person from one office or living space to another"""

    #     available_livingspace = [living_space.name.upper() for living_space in self.living_spaces if len(
    #         living_space.occupants) < living_space.capacity]
    #     available_offices = [office.name.upper() for office in self.offices if len(
    #         office.occupants) < office.capacity]

    #     # Check if the person exists

    #     fellow_names = [fellow.name.upper() for fellow in self.fellows]
    #     staff_names = [staff_details.name.upper() for staff_details in self.staff]

    #     if person_name not in fellow_names and person_name not in staff_names:
    #         msg = " The person {} does not exist ".format(person_name)
    #         print(msg)
    #         return msg

    #     elif r_room.upper() not in available_offices and r_room.upper(
    #     ) not in available_livingspace:
    #         msg = " The room {} does not exist or isn't available ".format(
    #             r_room)
    #         print(msg)
    #         return msg
    #     else:

    #         if r_room.upper() in available_offices and r_room.upper() not in available_livingspace:
    #             # new_office = [
    #             #             room_details.name for room_details in self.offices if room_details.name == r_room]

    #             current_office_index = [index for index in range(len(self.offices)) if person_name in self.offices[index].occupants]
    #             new_office_index = [index for index in range(len(self.offices)) if self.offices[index].name == r_room]
    #             import pdb; pdb.set_trace()

    #             if new_office_index:
    #                 new_office_index = new_office_index[0]
    #                 current_office_index = current_office_index[0:]

    #                 self.offices[current_office_index].occupants.remove(person_name)
    #                 self.offices[new_office_index].occupants.append(person_name)

    #                 # for room in self.offices:
    #                 #     if person_name in room.occupants:
    #                 #         c_offices = room.name
    #                 #         c_offices.remove(person_name)
    #                 #         new_office.occupants.append(person_name)
    #                 #         msg = "{} successfully reallocated to {}".format(
    #                 #             person_name, new_office)
    #                 #         print(msg)
    #                 #         return msg
    #                 msg = "{} successfully reallocated to {}".format(
    #                                 person_name, self.offices[new_office_index].name)
    #                 print(msg)
    #                 return msg
    #             else:
    #                 msg = "The room {} has to be an office"
    #                 print(msg)
    #                 return msg

    #         elif r_room.upper() in available_livingspace and r_room.upper() not in available_offices:
    #             if person_name in fellow_names:

    #                 new_livingspace = [
    #                         room_details.name for room_details in self.living_spaces if room_details.name == r_room]
    #                 if new_livingspace:
    #                     for room in self.living_spaces:
    #                         if person_name in room.occupants:
    #                             c_livingspace = room.name
    #                             c_livingspace.remove(person_name)
    #                             new_livingspace.occupants.append(person_name)
    #                             msg = "{} successfully reallocated to {}".format(
    #                                 person_name, new_livingspace)
    #                             print(msg)
    #                             return msg
    #                 else:
    #                     msg = "The room {} has to be an living space"
    #                     print(msg)
    #                     return msg
    #         else:
    #             msg = "Neither an office nor a living space"
    #             print(msg)
    #             return msg
            # else:

            #     # if name not in self.fellows:
            #     #     msg = " {} must be added and has to be a fellow ".format(
            #     #         name)
            #     #     print(msg)
            #     #     return msg
            #     # elif name not in self.staff:
            #     #     msg = " {} must be added and has to be a staff member".format(
            #     #         name)
            #     #     print(msg)
            #     #     return msg

    #             else:
    #                 # new_livingspace = [
    #                 #     room_details.name for room_details in self.living_spaces if room_details.name == r_room]
    #                 # if new_livingspace:
    #                 #     for room in self.living_spaces:
    #                 #         if name in self.living_spaces[room]:
    #                 #             c_livingspace = self.living_spaces[room]
    #                 #             c_livingspace.remove(name)
    #                 #             new_livingspace.occupants.append(name)
    #                 #             msg = "{} successfully reallocated to {}".format(
    #                 #                 name, new_livingspace)
    #                 #             print(msg)
    #                 #             return msg

    #                 else:
    #                         # loop to find current living space
    #                     # new_office = [
    #                     #     room_details.name for room_details in self.offices if room_details.name == r_room]
    #                     # if new_office:
    #                     #     for room in self.offices:
    #                     #         if name in self.offices[room]:
    #                     #             c_offices = self.offices[room]
    #                     #             c_offices.remove(name)
    #                     #             new_office.occupants.append(name)
    #                     #             msg = "{} successfully reallocated to {}".format(
    #                     #                 name, new_office)
    #                     #             print(msg)
    #                     #             return msg
    #                     # else:
    #                     #     print('Neither office or living space')

    # # def print_allocations(self):
    # #     """ Print people and the rooms they have been allocated """
    # #     pass
    # #
    # # def save_allocations_to_file(self):
    # #     """ Save people and the rooms they have been allocated to file"""
    # #     pass
    # #
    # # def print_unallocated(self):
    # #     """ Print a list of people who have not been allocated a room"""
    # #     pass
