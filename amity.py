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
                return msg

            new_staff = Staff(person_id, name)
            self.staff.append(new_staff)
            allocation_office = self.allocate_office_space(new_staff)
            if isinstance(allocation_office, str):

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

                    msg = "The fellow {} has been successfully added and allocated the living space {} but sorry we do not have any available offices".format(
                        name, allocation_living_space.room_name)
                    puts(colored.yellow(msg))
                    return msg
                # Allocate only office and add the fellow to a waiting list
                elif not isinstance(allocation_office, str) and isinstance(
                        allocation_living_space, str):
                    # self.living_waitlist.append(new_fellow)
                    msg = "The fellow {} has been successfully added and allocated the office {} but sorry we do not have any available living spaces".format(
                        name, allocation_office.room_name)
                    puts(colored.yellow(msg))
                    return msg
                elif isinstance(allocation_office, str) and isinstance(
                        allocation_living_space, str):
                    msg = "The fellow {} has been successfully added and will be allocated an office and living space once they're available".format(
                        name)
                    puts(colored.yellow(msg))
                    return msg
            elif wants_accomodation == "N":
                self.fellows.append(new_fellow)
                allocation_office = self.allocate_office_space(new_fellow)
                if isinstance(allocation_office, str):
                    msg = allocation_office
                    puts(colored.red(msg))
                    return msg
                else:
                    msg = "The fellow {} has been successfully added and allocated the office {}".format(
                        name, allocation_office.room_name)
                    puts(colored.green(msg))
                    return msg

    def list_people(self):
        """ Method that lists all the people in Amity, showing their room(s) and role"""
        # TODO: Find a good way of displaying the room and role of the person
        msg = "\n\nLIST OF ALL STAFF \n" + "*" * 50 + "\n\n"
        if len(self.staff) == 0:
            msg += "There are currently no staff members!"
        else:
            for staff in self.staff:
                if staff.allocated is None:
                    o_allocated = "No Office"
                else:
                    o_allocated = staff.allocated
                msg += staff.name + "\t" + o_allocated + "\n"

        msg += "\n\nLIST OF ALL FELLOWS \n" + "*" * 50 + "\n\n"
        if len(self.fellows) == 0:
            msg += "There are currently no fellows!"
        else:
            for fellow in self.fellows:
                if fellow.accomodated is None:
                    l_accomodated = "No Livingspace"
                else:
                    l_accomodated = fellow.accomodated
                if fellow.allocated is None:
                    o_allocated = "No Office"
                else:
                    o_allocated = fellow.allocated
                msg += fellow.name + "\t" + o_allocated + "\t" + l_accomodated + "\n"
        puts(colored.cyan(msg))
        return "List Printed Successfully"

    def delete_person(self, f_name, l_name):
        """ Deletes a person from the Amity system"""
        all_people = self.fellows + self.staff
        all_rooms = self.offices + self.living_spaces
        name = f_name + " " + l_name
        name = name.upper()
        msg = ""

        # Loop through all people to find the room they are in
        deleted_person = [
            person for person in all_people if person.name.upper() == name
        ]
        if len(deleted_person) == 0:
            msg = "The person {} does not exist".format(name)
            return msg

        person_room = [
            room for room in all_rooms if deleted_person[0] in room.occupants
        ]

        if len(person_room) != 0:
            if isinstance(deleted_person[0], Staff):
                self.staff.remove(deleted_person[0])
                person_room[0].occupants.remove(deleted_person[0])
            else:
                self.fellows.remove(deleted_person[0])
                person_room[0].occupants.remove(deleted_person[0])
                if len(person_room) == 2:
                    person_room[1].occupants.remove(deleted_person[0])
            if deleted_person[0] in self.office_waitlist:
                self.office_waitlist.remove(deleted_person[0])

            if deleted_person[0] in self.living_waitlist:
                self.living_waitlist.remove(deleted_person[0])

            msg = "{} has been successfully deleted from Amity.".format(name)
            puts(colored.green(msg))
            return msg
        else:
            if isinstance(deleted_person[0], Staff):
                self.staff.remove(deleted_person[0])
            else:
                self.fellows.remove(deleted_person[0])
            msg = "{} has been successfully deleted from Amity.".format(name)
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
            response += ("\n\nLIST OF EACH LIVING SPACE AND IT'S OCCUPANTS\n" +
                         "*" * 50 + "\n")
            for room in self.living_spaces:
                response += room.room_name.upper() + "\n" + ("*" * 50 + "\n")
                people = [person.name for person in room.occupants]
                response += ", ".join(people) + "\n\n\n\n"

            if len(self.offices) == 0:
                response += "There are currently no offices"

            else:
                response += ("\n\nLIST OF EACH OFFICE AND IT'S OCCUPANTS\n" +
                             "*" * 50 + "\n")
                for room in self.offices:
                    response += room.room_name.upper() + "\n" + ("*" * 50 + "\n")
                    people = [person.name for person in room.occupants]
                    response += ", ".join(people) + "\n\n\n\n"
        if not filename:
            puts(colored.magenta(response))
            return response
        else:
            puts(colored.green("Saving output data to file..."))
            txt_file = open(filename + ".txt", "w+")
            txt_file.write(response)
            txt_file.close()
            msg = "\nData has been successfully saved to {}.txt\n".format(
                filename)
            puts(colored.magenta(msg))
            return msg

    def print_unallocated(self, filename=None):
        """ This method prints a list of all staff and fellows, that have not been allocated any office or living space. """
        total_waitlist = self.office_waitlist + self.living_waitlist
        response = ""

        # Check if there are any unnalocated people
        if len(total_waitlist) == 0:
            msg = "There are no unallocated staff or fellows"
            puts(colored.yellow(msg))
            return msg

        else:
            puts(colored.cyan("\n\nLIST OF ALL UNALLOCATED STAFF AND FELLOWS\n" + "*" * 50
                              + "\n"))
            for person in self.office_waitlist:
                if isinstance(person, Staff):
                    role = "STAFF"
                else:
                    role = "FELLOW"
                response += (
                    person.name + "\t" + role + "\t" + "OFFICE SPACE" + "\n")
            for person in self.living_waitlist:
                response += (
                    person.name + "\t" + "FELLOW" + "\t" + "LIVING SPACE" + "\n")

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
            puts(colored.magenta(response))
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
                f_name = word_list[0]
                l_name = word_list[1]
                role = word_list[2]
                if len(word_list) != 4:
                    wants_accomodation = "N"
                else:
                    wants_accomodation = word_list[3]
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
        # import ipdb; ipdb.set_trace()

        new_room = [
            room for room in all_rooms if room.room_name == new_room_name
        ]
        if len(new_room) == 0:
            msg = "The room {} does not exist".format(new_room_name)
            return msg

        reallocated_person = [
            person for person in all_people if person.name.upper() == name
        ]
        if len(reallocated_person) == 0:
            msg = "The person {} does not exist".format(name)
            return msg

        current_room = [
            room for room in all_rooms
            if reallocated_person[0] in room.occupants
        ]

        if len(current_room) == 0:
            current_room = None
        # Check if the person is a staff member looking for a living space
        if name in [person.name for person in self.staff] and new_room_name in [room.room_name for room in self.living_spaces]:
            msg = "A staff member cannot be allocated a living space"
            return msg

        elif new_room == current_room:
            msg = "Cannot reallocate to the same room"
            return msg

        else:
            if current_room is None:
                new_room[0].occupants.append(reallocated_person[0])
                if isinstance(new_room[0], Office):
                    reallocated_person[0].allocated = new_room[0].room_name
                else:
                    reallocated_person[0].accomodated = new_room[0].room_name

                msg = "{} has been successfully reallocated to {}".format(
                    name, new_room_name)

                return msg
            else:
                current_room[0].occupants.remove(reallocated_person[0])
                new_room[0].occupants.append(reallocated_person[0])
                if isinstance(new_room[0], Office):
                    reallocated_person[0].allocated = new_room[0].room_name
                else:
                    reallocated_person[0].accomodated = new_room[0].room_name

                msg = "{} has been successfully reallocated to {}".format(
                    name, new_room_name)
                return msg

    def delete_room(self, room_name):
        """ This method deletes a room from the Amity app"""
        all_people = self.staff + self.fellows
        all_rooms = self.offices + self.living_spaces
        room_name = room_name.upper()

        deleted_room = [
            room for room in all_rooms if room.room_name == room_name]
        if len(deleted_room) == 0:
            msg = "The room {} does not exist".format(room_name)
            puts(colored.red(msg))
            return msg
        else:
            deleted_room = deleted_room[0]
            if isinstance(deleted_room, Office):
                for person in deleted_room.occupants:
                    person.allocated = None
                    self.office_waitlist.append(person)
                self.offices.remove(deleted_room)
            else:
                for person in deleted_room.occupants:
                    person.accomodated = None
                    self.living_waitlist.append(person)
                self.living_spaces.remove(deleted_room)
        msg = "The room {} has been deleted from Amity.".format(room_name)
        puts(colored.green(msg))
        return msg

    def update_database(self, database_name=None):
        """ Method that updates given database: Helper function for save_state()"""
        # TODO: create the method XD
        # TODO: Method should determine which are the affected rows and columns and update them
        # TODO: Learn SQL Alchemy to be able to do this seamlessly

    def save_state(self, database_name=None):
        """ Method that saves all the data into a given database """
        all_rooms = self.offices + self.living_spaces
        all_people = self.fellows + self.staff
        if not database_name:
            database = CreateDb("amity")
        else:
            database = CreateDb(database_name)

        Base.metadata.bind = database.engine
        database_session = database.session()
        database_session.query(PersonModel).delete()
        database_session.query(RoomModel).delete()

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
        puts(colored.green(msg))
        return msg


    def load_state(self, database_name=None):
        """ Method that loads the saved state """
        all_rooms = self.offices + self.living_spaces
        all_people = self.staff + self.fellows
        msg = ""

        engine = create_engine("sqlite:///" + database_name + ".db")
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        try:
            guys = session.query(PersonModel).all()
            their_rooms = session.query(RoomModel).all()

        except:
            msg = "Sorry wrong database format"
            puts(colored.yellow(msg))
            return msg

        for guy in guys:
            if guy.id not in [this_guy.person_id for this_guy in all_people]:
                if guy.role == "STAFF":
                    staff = Staff(guy.id, guy.name)
                    self.staff.append(staff)
                    staff.allocated = guy.office_space
                else:
                    fellow = Fellow(guy.id, guy.name)
                    self.fellows.append(fellow)
                    fellow.allocated = guy.office_space
                    fellow.accommodated = guy.living_space
            else:
                msg += "The person {} already exists\n".format(guy.name)
        all_people = self.fellows + self.staff
        for room in their_rooms:
            # looping to check if the room already exists in amity
            if room.name not in [this_room.room_name for this_room in all_rooms]:
                if room.room_type == "OFFICE":
                    office = Office(room.name)  # create new office
                    self.offices.append(office)  # add to list of offices
                    guys_in_room = session.query(PersonModel.name).filter(
                        PersonModel.office_space == room.name).all()
                    guys_in_room = [str(i[0]) for i in guys_in_room]
                    folks_in_room = [
                        you_guy for you_guy in all_people if you_guy.name in guys_in_room]
                    office.occupants = folks_in_room
                else:
                    livingspace = Living_Space(
                        room.name)  # create living space
                    # add to list of living spaces
                    self.living_spaces.append(livingspace)
                    guys_in_room = session.query(PersonModel.name).filter(
                        PersonModel.living_space == room.name).all()
                    guys_in_room = [str(i[0]) for i in guys_in_room]
                    # loop to get the actual person object
                    folks_in_room = [
                        you_guy for you_guy in all_people if you_guy.name in guys_in_room]
                    livingspace.occupants = folks_in_room

            else:
                msg += "The room {} already exists \n".format(room.name)

        puts(colored.yellow(msg))
        success = "Data loaded successfully!\n"
        puts(colored.cyan(success))
        return success + msg
