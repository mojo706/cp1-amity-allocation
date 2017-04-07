""" Contains tests for the main amity class and most of it's functions"""
import unittest
import os
from amity_functions import Amity


class TestAmity(unittest.TestCase):
    """ Class that contains test for the funtions defined in amity.py """

    def setUp(self):
        self.amity = Amity()
        # self.amity.create_room("OFFICE", "Addis")
        # self.amity.create_room("OFFICE", "Accra")
        # self.amity.create_room("LIVINGSPACE", "Valhala")
        # self.amity.create_room("LIVINGSPACE", "Camelot")
        self.amity.all_rooms = ["Addis", "Valhala", "Camelot", "Accra"]

    def test_input_can_only_be_string(self):
        """ test whether the input is a string or not"""
        # Test wrong room type
        with self.assertRaises(ValueError):
            self.amity.create_room(2, "Tsavo")

        # Test wrong room name
        with self.assertRaises(ValueError):
            self.amity.create_room("Office", {})

    def test_existing_room_name(self):
        room_msg = self.amity.create_room("OFFICE", "Accra")
        expected = "The room Accra has already been created"
        self.assertEqual(room_msg, expected)

    def test_office_created(self):
        """ test if office is successfully created"""
        offices = len(self.amity.offices)
        self.amity.create_room("OFFICE", "Hogwarts")
        self.assertEqual(len(self.amity.offices), offices + 1)

    def test_living_space_created(self):
        """ test whether living room is created """
        living_spaces = len(self.amity.living_spaces)
        self.amity.create_room("LIVINGSPACE", "Php")
        self.assertEqual(len(self.amity.living_spaces), living_spaces + 1)

    def test_add_person(self):
        """ test whether person has been successfully added """
        all_people = len(self.amity.all_people)
        fellow = self.amity.add_person("Omar", "FELLOW")
        expected_output = "The person Omar has been successfully added"
        self.assertEqual(fellow, expected_output)

    def test_allocate_person_to_room(self):
        """ Allocate a person an office or living space """
        pass

    def test_adding_fellow(self):
        """ Is the fellow added successfully"""
        initial_fellow_count = len(self.amity.fellows)
        self.amity.add_person("Chuchu Omar", "")
        new_fellow_count = len()

    def test_adding_staff(self):
        """ Is the staff added successfully"""
        initial_staff_count = len(self.amity.all_staff)

        new_staff_count = len(self.amity.all_staff)
        self.assertEqual(
            new_staff_count - initial_staff_count,
            1,
            msg="Failed to add new staff")

    def test_reallocate_person(self):
        """ Move a person from one office space or living space to another"""

    def test_reallocation_fails_if_room_doesnt_exist(self):
        """ Cannot reallocate to a non-existent room """
        res = self.amity.reallocate_person("chuchu@chuchu", "The_Tsavo")
        self.assertEqual(res, "The room The_Tsavo does not exist!")

    def test_print_allocations(self):
        """ Print people and the rooms they have been allocated """

    def test_print_unallocated(self):
        """ Print a list of people who have not been allocated a room"""

    def test_save_allocations_to_file(self):
        """ Save people and the rooms they have been allocated to file"""
