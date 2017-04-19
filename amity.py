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

    def create_room(self, room_type, room_name):
        """Create a new room, a room can either be an office or living_space,
        then check to make sure no room with the same name exits
         before successfully creating the room
        """
        all_rooms = self.offices + self.living_spaces

        if not isinstance(room_name, str) or not isinstance(room_type, str):
            raise ValueError("Invalid Input")

        if room_name in [room.room_name for room in all_rooms]:
            msg = "The room {} has already been created".format(room_name)
            print(msg)
            return msg

        if room_type.upper() == "OFFICE":
            new_office = Office(room_name)
            self.offices.append(new_office)
            msg = "Office Successfully Created"
            print(msg)
            return msg

        if room_type.upper() == "LIVINGSPACE":
            new_living_space = Living_Space(room_name)
            self.living_spaces.append(new_living_space)
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
            person.allocated = allocated_room.room_name
            return allocated_room
        else:
            self.office_waitlist.append(person)
            return "No available offices"

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
            person.accomodated = allocated_room.room_name
            return allocated_room
        else:
            self.living_waitlist.append(person)
            return "No available living space"

    def add_person(self, name, role, wants_accomodation="N"):
        """ Add person to Amity and assign them an office space or
        living space"""
        # person_id = random.randint(1000, 9999)
        person_id = 1
        roles = ["STAFF", "FELLOW"]
        role = role.upper()
        name = name.upper()
        if not isinstance(name, str) and not isinstance(role, str):
            raise ValueError(" Name and Role must be string")

        if role not in roles:
            raise ValueError("Invalid Role")

        if role == "STAFF":
            if name in self.staff:
                msg = "That Staff member already exists"
                print(msg)
                return msg
            new_staff = Staff(person_id, name)
            self.staff.append(new_staff)
            allocation_office = self.allocate_office_space(new_staff)
            if isinstance(allocation_office, str):
                self.office_waitlist.append(new_staff)
                msg = allocation_office
                print(msg)
                return msg
            else:
                msg = "The staff member {} has been successfully added and allocated the office {}".format(
                    name, allocation_office.room_name)
                print(msg)
                return msg

        elif role == "FELLOW":

            if name in self.fellows:
                msg = "That Fellow already exists"
                print(msg)
                return msg
            new_fellow = Fellow(person_id, name)

            if wants_accomodation == "Y":
                self.fellows.append(new_fellow)
                allocation_office = self.allocate_office_space(new_fellow)
                allocation_living_space = self.allocate_living_space(
                    new_fellow)
                # Allocate both living and office space
                if not isinstance(allocation_office, str) and not isinstance(allocation_living_space, str):
                    msg = "The fellow {} has been successfully added and allocated the office {} and the living space {}".format(
                        name, allocation_office.room_name, allocation_living_space.room_name)
                    print(msg)
                    return msg
                # Allocate only living space and add the fellow to a waiting
                # list
                elif isinstance(allocation_office, str) and not isinstance(allocation_living_space, str):
                    self.office_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and allocated the living space {} but sorry we do not have any available offices".format(
                        name, allocation_living_space.room_name)
                    print(msg)
                    return msg
                # Allocate only office and add the fellow to a waiting list
                elif not isinstance(allocation_office, str) and isinstance(allocation_living_space, str):
                    self.living_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and allocated the office {} but sorry we do not have any available living spaces".format(
                        name, allocation_office.room_name)
                    print(msg)
                    return msg
                elif isinstance(allocation_office, str) and isinstance(allocation_living_space, str):
                    self.living_waitlist.append(new_fellow)
                    self.office_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and will be allocated an office and living space once they're available".format(
                        name)
                    print(msg)
                    return msg
            elif wants_accomodation == "N":
                self.fellows.append(new_fellow)
                allocation_office = self.allocate_office_space(new_fellow)
                if isinstance(allocation_office, str):
                    self.office_waitlist.append(new_fellow)
                    msg = allocation_office
                    print(msg)
                    return msg
                else:
                    msg = "The fellow {} has been successfully added and allocated the office {}".format(
                        name, allocation_office.room_name)
                    print(msg)
                    return msg
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

    # def allocate_unallocated(self, room_type, room_name):
    #     """ used to allocate fellows or staff who were previously
    #     unallocated """
    #     allocations = []
    #     if room_type.upper() == "LIVINGSPACE":
    #         for person in self.living_waitlist:
    #             print(self.allocate_living_space(person))
    #             if self.person_status:
    #                 allocations.append(person)
    #     # Update living space waiting list
    #     new_living_waitlist = list(
    #         set(self.living_waitlist) - set(allocations))
    #     self.living_waitlist = new_living_waitlist

    #     if room_type.upper() == "OFFICE":
    #         for person in self.office_waitlist:
    #             print(self.allocate_office_space(person))
    #             if self.person_status:
    #                 allocations.append(person)
    #     # Update office waiting list
    #     new_office_waitlist = list(
    #         set(self.office_waitlist) - set(allocations))
    #     self.office_waitlist = new_office_waitlist

    def reallocate_person(self, person_id, new_room_name):
        """ This method is used to reallocate a person from one room to another"""
        all_people = self.fellows + self.staff
        all_rooms = self.offices + self.living_spaces
        import pdb
        pdb.set_trace()

        try:
            new_room = [
                room for room in all_rooms if room.room_name == new_room_name]
        except:
            msg = "The room {} does not exist".format(new_room_name)
            print(msg)
            return msg
        try:
            reallocated_person = [
                person for person in all_people if person.person_id == person_id]
        except:
            msg = "The person with ID {} does not exist".format(person_id)
            print(msg)
            return msg
        try:
            current_room = [
                room for room in all_rooms if reallocated_person[0] in room.occupants]
        except:
            current_room = None

        # Check if the person is a staff member looking for a living space
        if person_id in [person.person_id for person in self.staff] and new_room_name in [room.room_name for room in self.living_spaces]:
            msg = "A staff member cannot be allocated a living space"
            print(msg)
            return msg

        elif new_room == current_room:
            msg = "Cannot reallocate to the same room"
            print(msg)
            return msg

        else:
            if current_room == None:
                new_room.occupants.append(reallocated_person[0])
                msg = "{} has been successfully reallocated to {}".format(
                    reallocated_person[0].name, new_room_name)
                print(msg)
                return msg
            else:
                current_room[0].occupants.remove(reallocated_person[0])
                new_room[0].occupants.append(reallocated_person[0])
                msg = "{} has been successfully reallocated to {}".format(
                    reallocated_person[0].name, new_room_name)
                print(msg)
                return msg
