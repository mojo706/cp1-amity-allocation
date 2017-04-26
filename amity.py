""" This file contains all the functions of the amity cli app """

import os
import random

from person.persons import Fellow, Staff
from room.rooms import Room, Office, Living_Space
from model.models import Base, CreateDb, PersonModel, RoomModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from clint.textui import colored, puts


class Amity(object):
    """ Main Class for all the methods the other classes to inherit from """

    def __init__(self):
        self.offices = []
        self.living_spaces = []
        self.fellows = []
        self.staff = []
        self.office_waitlist = []
        self.living_waitlist = []
        # self.all_rooms = self.offices + self.living_spaces

    def create_room(self, room_type, room_name):
        """Create a new room, a room can either be an office or living_space,
        then check to make sure no room with the same name exits
         before successfully creating the room
        """
        room = []
        office_name_list = [room.room_name for room in self.offices]
        livingspace_name_list = [room.room_name for room in self.living_spaces]
        room_name = room_name.upper()

        if not room_name.isalpha():
            msg = "Invalid Input For Room Name"
            puts(colored.red(msg))
            return msg

        elif not room_type.isalpha():
            msg = "Invalid Input For Room Type"
            puts(colored.red(msg))
            return msg

        elif room_name in office_name_list or room_name in livingspace_name_list:
            msg = "The room {} has already been created".format(room_name)
            puts(colored.yellow(msg))
            return msg

        elif room_type.upper() == "OFFICE":
            new_office = Office(room_name)
            self.offices.append(new_office)
            room.append(room_name)
            msg = "The Office {} was created successfully".format(room_name)
            puts(colored.green(msg))
            return msg

        elif room_type.upper() == "LIVINGSPACE":
            new_living_space = Living_Space(room_name)
            self.living_spaces.append(new_living_space)
            room.append(room_name)
            msg = "The Living Space {} was created successfully".format(
                room_name)
            puts(colored.green(msg))
            return msg

        else:
            msg = "Room type can only be an office or a living space"
            puts(colored.yellow(msg))
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

    def add_person(self, f_name, l_name, role, wants_accomodation="N"):
        """ Add person to Amity and assign them an office space or
        living space"""
        person_id = random.randint(1000, 9999)
        roles = ["STAFF", "FELLOW"]
        role = role.upper()
        name = f_name + " " + l_name
        name = name.upper()

        if not (f_name + l_name).isalpha():
            return "First and Last name must be alphabets"

        if role not in roles:
            return "Invalid Role"

        if role == "STAFF":
            no_living = ""
            if wants_accomodation == "Y":
                no_living = " Sorry a staff member cannot be assigned a living space"

            if name in [staff.name for staff in self.staff]:
                msg = "That Staff member already exists"
                puts(colored.yellow(msg))

            new_staff = Staff(person_id, name)
            self.staff.append(new_staff)
            allocation_office = self.allocate_office_space(new_staff)
            if isinstance(allocation_office, str):
                self.office_waitlist.append(new_staff)
                msg = "The staff member {} has been successfully added and will be allocated an office once it's available.".format(
                    new_staff.name)
                puts(colored.yellow(msg + no_living))
                return msg + no_living
            else:
                msg = "The staff member {} has been successfully added and allocated the office {}.".format(
                    name, allocation_office.room_name)
                puts(colored.green(msg + no_living))
                return msg + no_living

        elif role == "FELLOW":

            if name in [fellow.name for fellow in self.fellows]:
                msg = "That Fellow already exists"
                puts(colored.yellow(msg))
                return msg
            new_fellow = Fellow(person_id, name)

            if wants_accomodation == "Y":
                self.fellows.append(new_fellow)
                allocation_office = self.allocate_office_space(new_fellow)
                allocation_living_space = self.allocate_living_space(
                    new_fellow)
                # Allocate both living and office space
                if not isinstance(allocation_office, str) and not isinstance(
                        allocation_living_space, str):
                    msg = "The fellow {} has been successfully added and allocated the office {} and the living space {}".format(
                        name, allocation_office.room_name,
                        allocation_living_space.room_name)
                    puts(colored.green(msg))
                    return msg
                # Allocate only living space and add the fellow to a waiting
                # list
                elif isinstance(allocation_office, str) and not isinstance(
                        allocation_living_space, str):
                    self.office_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and allocated the living space {} but sorry we do not have any available offices".format(
                        name, allocation_living_space.room_name)
                    puts(colored.yellow(msg))
                    return msg
                # Allocate only office and add the fellow to a waiting list
                elif not isinstance(allocation_office, str) and isinstance(
                        allocation_living_space, str):
                    self.living_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and allocated the office {} but sorry we do not have any available living spaces".format(
                        name, allocation_office.room_name)
                    puts(colored.yellow(msg))
                    return msg
                elif isinstance(allocation_office, str) and isinstance(
                        allocation_living_space, str):
                    self.living_waitlist.append(new_fellow)
                    self.office_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and will be allocated an office and living space once they're available".format(
                        name)
                    puts(colored.yellow(msg))
                    return msg
            elif wants_accomodation == "N":
                self.fellows.append(new_fellow)
                allocation_office = self.allocate_office_space(new_fellow)
                if isinstance(allocation_office, str):
                    self.office_waitlist.append(new_fellow)
                    msg = allocation_office
                    puts(colored.red(msg))
                    return msg
                else:
                    msg = "The fellow {} has been successfully added and allocated the office {}".format(
                        name, allocation_office.room_name)
                    puts(colored.green(msg))
                    return msg

    def delete_person(self, name):
        """ Deletes a person from the Amity system"""
        all_people = self.fellows + self.staff
        all_rooms = self.offices + self.living_spaces
        # Loop through all people to find the room they are in
        try:
            deleted_person = [
                person for person in all_people if person.name.upper() == name
            ]
        except BaseException:
            msg = "The person {} does not exist".format(name)
            return msg

        person_room = [
            room for room in all_rooms
            if deleted_person[0] in room.occupants]

        person_room[0].occupants.remove(deleted_person[0])
        msg = "{} has been successfully deleted from Amity."
        puts(colored.green(msg))
        return msg


    def print_room(self, room_name):
        """ Prints the names of all the people in a room on the
             screen """
        # import pdb; pdb.set_trace()
        all_rooms = self.living_spaces + self.offices
        room_name = room_name.upper()
        room_occupants = [
            room.occupants for room in all_rooms if room.room_name == room_name
        ]
        office_name_list = [room.room_name for room in self.offices]
        livingspace_name_list = [room.room_name for room in self.living_spaces]

        # msg = ""

        # Check if room name exists
        if room_name not in office_name_list and room_name not in livingspace_name_list:
            msg = "The room {} doesn't exist ".format(room_name.upper())
            puts(colored.red(msg))
            return msg
        if len(room_occupants[0]) == 0:
            msg = "Room is empty"
            puts(colored.yellow(msg))
            return msg
        else:
            msg = "The Occupants in {} are: ".format(room_name)
            for person in room_occupants[0]:
                msg += "\n {} ".format(person.name)
                puts(colored.green(msg))
            return msg

    def print_allocations(self, filename=None):
        """ Prints a list of allocations onto the screen. Specifying the optional -o option here outputs the registered allocations to a txt file."""
        response = ""
        if len(self.living_spaces) == 0:
            response = "There are currently no living spaces\n\n"

        else:
            puts(
                colored.blue(
                    "\n\nLIST OF EACH LIVING SPACE AND IT'S OCCUPANTS\n")) + (
                        colored.cyan("*" * 50 + "\n"))
            for room in self.living_spaces:
                response += room.room_name.upper() + "\n" + ("*" * 50 + "\n")
                people = [person.name for person in room.occupants]
                response += ", ".join(people) + "\n\n\n\n"

        if len(self.offices) == 0:
            response += "There are currently no offices"

        else:
            puts(colored.blue("\n\nLIST OF EACH OFFICE AND IT'S OCCUPANTS\n")
                 ) + (colored.cyan("*" * 50 + "\n"))
            for room in self.offices:
                response += room.room_name.upper() + "\n"
                puts(colored.cyan("*" * 50 + "\n"))
                people = [person.name for person in room.occupants]
                response += ", ".join(people) + "\n\n\n\n"
        if not filename:
            puts(colored.green(response))
            return response
        else:
            puts(colored.green("Saving output data to file..."))
            txt_file = open(filename + ".txt", "w+")
            txt_file.write(response)
            txt_file.close()
            msg = "\nData has been successfully saved to {}.txt\n".format(
                filename)
            puts(colored.green(msg))
            return msg
            # return ("\nData has been successfully saved to {}.txt\n"
            #         .format(filename))

    def print_unallocated(self, filename=None):
        """ This method prints a list of all staff and fellows, that have not been allocated any office or living space. """
        total_waitlist = self.office_waitlist + self.living_waitlist
        response = ""

        # Check if there are any unnalocated people
        if len(total_waitlist) == 0:
            msg = "There are no unallocated staff or fellows"
            print(msg)
            return msg

        else:
            print("\n\nLIST OF ALL UNALLOCATED STAFF AND FELLOWS\n" + "*" * 50
                  + "\n")
            for person in self.office_waitlist:
                if isinstance(person, Staff):
                    role = "STAFF"
                else:
                    role = "FELLOW"
                response += (
                    person.name + "\t" + role + "\t" + "OFFICE SPACE" + "\n")
            for person in self.living_waitlist:
                response += (
                    person.name + "\t" + role + "\t" + "LIVING SPACE" + "\n")

        if filename:
            # create file with the given filename and write res to it
            puts(colored.cyan("Saving unallocations list to file..."))
            txt_file = open(filename + ".txt", "w+")
            txt_file.write(response)
            txt_file.close()
            msg = "Data has been successfully saved to {}.txt".format(filename)
            puts(colored.green(msg))
            return msg
        else:
            print(response)
            # return response

    def load_people(self, filename):
        """ This method adds people to rooms from a txt file. """
        amitypath = os.path.dirname(__file__)
        filepath = os.path.join(amitypath, filename + ".txt")
        if not os.path.isfile(filepath):
            msg = "{} is not a valid file path.".format(filepath)
            print(msg)
            return msg
        with open(filepath, 'r') as f:
            for line in f:
                word_list = line.split()
                # print(word_list)
                f_name = word_list[0]
                l_name = word_list[1]
                role = word_list[2]
                if len(word_list) != 4:
                    wants_accomodation = "N"
                else:
                    wants_accomodation = word_list[3]
                # print(wants_accomodation)
                self.add_person(f_name, l_name, role, wants_accomodation)
        msg = "People were loaded successfully!"
        print(msg)
        return msg

    def reallocate_person(self, f_name, l_name, new_room_name):
        """ This method is used to reallocate a person from one room to another"""
        all_people = self.fellows + self.staff
        all_rooms = self.offices + self.living_spaces
        name = f_name + " " + l_name
        name = name.upper()
        new_room_name = new_room_name.upper()

        try:
            new_room = [
                room for room in all_rooms if room.room_name == new_room_name
            ]
        except BaseException:
            msg = "The room {} does not exist".format(new_room_name)
            return msg

        try:
            reallocated_person = [
                person for person in all_people if person.name.upper() == name
            ]
        except BaseException:
            msg = "The person {} does not exist".format(name)
            return msg
        try:
            current_room = [
                room for room in all_rooms
                if reallocated_person[0] in room.occupants
            ]
        except BaseException:
            current_room = None
        # Check if the person is a staff member looking for a living space
        if name in [person.name
                    for person in self.staff] and new_room_name in [
                        room.room_name for room in self.living_spaces
                    ]:
            msg = "A staff member cannot be allocated a living space"
            return msg

        elif new_room == current_room:
            msg = "Cannot reallocate to the same room"
            return msg

        else:
            if len(current_room) == 0:
                new_room[0].occupants.append(reallocated_person[0])
                msg = "{} has been successfully reallocated to {}".format(
                    name, new_room_name)
                return msg
            else:
                current_room[0].occupants.remove(reallocated_person[0])
                new_room[0].occupants.append(reallocated_person[0])
                msg = "{} has been successfully reallocated to {}".format(
                    name, new_room_name)
                return msg

    def delete_room(self, room):
        """ This method deletes a room from the Amity app"""
        all_people = self.staff + self.fellows
        all_rooms = self.offices + self.living_spaces

        deleted_room = [room for room in all_rooms if room.room_name == room]

        # TODO: check if room is office or living_space
        # TODO: loop through all occupant in room and append them to relevant waiting list
        # TODO: delete the room from amity

    def update_database(self, database_name=None):
        """ Method that updates given database: Helper function for save_state()"""
        # TODO: create the method XD
        # TODO: Method should determine which are the affected rows and columns and update them
        # TODO: Learn SQL Alchemy to be able to do this seamlessly
    def list_people(self):
        """ Method that list all the people in Amity, showing their room(s) and role"""
        # TODO: Find a good way of displaying the room and role of the person

    def save_state(self, database_name=None):
        """ Method that saves all the data into a given database """
        all_rooms = self.offices + self.living_spaces
        all_people = self.fellows + self.staff
        if not database_name:
            database = CreateDb("amity")
        else:
            database = CreateDb(database_name)

        Amity.clear_db(database_name)
        Base.metadata.bind = database.engine
        database_session = database.session()
        for room in all_rooms:
            saved_room = RoomModel(
                name=room.room_name,
                room_type=room.room_type,
                room_capacity=room.capacity)
            database_session.merge(saved_room)
        for person in all_people:
            if isinstance(person, Staff):
                saved_person = PersonModel(
                    id=person.person_id,
                    name=person.name,
                    role="STAFF",
                    office_space=person.allocated,
                    living_space=None)
            else:
                saved_person = PersonModel(
                    id=person.person_id,
                    name=person.name,
                    role="FELLOW",
                    office_space=person.allocated,
                    living_space=person.accomodated)
            database_session.merge(saved_person)
        database_session.commit()
        msg = "State Saved Successfully"
        print(msg)
        return msg

    def load_state(self, database_name=None):
        """ Method that loads the saved state """

        engine = create_engine("sqlite:///" + database_name + ".db")
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        all_people = session.query(PersonModel).all()
        all_rooms = session.query(RoomModel).all()

        if not database_name:
            print("You must select a database to load from")
        else:
            for room in all_rooms:
                if room.room_type == "LIVING SPACE":
                    living_space = Living_Space(room.name)
                    # current_occupants = session.query(PersonModel.name).filter(
                    #     PersonModel.living_space == room.name).all()
                    # occupants_in_room = []
                    # for person in current_occupants:
                    #     occupants_in_room.append(str(person[0]))
                    # living_space.occupants = occupants_in_room
                    self.living_spaces.append(living_space)
                else:
                    office_space = Living_Space(room.name)
                    # current_occupants = session.query(PersonModel.name).filter(
                    #     PersonModel.office_space == room.name).all()
                    # occupants_in_room = []
                    # for person in current_occupants:
                    #     occupants_in_room.append(str(person[0]))
                    self.offices.append(office_space)
            for person in all_people:
                if person.role == "FELLOW":
                    fellow = Fellow(person.id, person.name)
                    self.fellows.append(fellow)
                    person_name = person.name.split(' ')
                    # person_ls = [
                    #     room for room in self.living_spaces if room.name == person.living_space]
                    # person_ls = person_ls[0]
                    # person.accomodated = person_ls
                    if person.living_space is not None:
                        self.reallocate_person(person_name[0], person_name[1],
                                               person.living_space)
                    else:
                        self.living_waitlist.append(fellow)

                    if person.office_space is not None:
                        self.reallocate_person(person_name[0], person_name[1],
                                               person.office_space)

                    else:
                        self.office_waitlist.append(fellow)
                else:
                    staff = Staff(person.id, person.name)
                    self.staff.append(staff)
                    person_name = person.name.split(' ')
                    if person.office_space is not None:
                        self.reallocate_person(person_name[0], person_name[1],
                                               person.office_space)

                    else:
                        self.office_waitlist.append(staff)
            msg = "Data from {} loaded Successfully!.".format(database_name)
            print(msg)
            return msg

    def clear_db(self, database_name=''):
        """
        Method to clear DB before save state
        """

        if database_name:

            name = database_name

        else:

            name = 'amity_db'

        Session = sessionmaker()

        engine = create_engine("sqlite:///" + database_name + ".db")

        Session.configure(bind=engine)

        # Drop all tables then recreate them.

        Base.metadata.drop_all(bind=engine)

        Base.metadata.create_all(bind=engine)

        return 'Database cleared successfully.'
