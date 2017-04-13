""" Contains tests for the main amity class and most of it's functions"""
import unittest
import os
from amity import Amity


class TestAmity(unittest.TestCase):
    """ Class that contains test for the funtions defined in amity.py """

    def setUp(self):
        self.amity = Amity()
        self.amity.create_room("OFFICE", "Addis")
        self.amity.create_room("OFFICE", "Accra")
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("LIVINGSPACE", "Camelot")

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
        room_msg = self.amity.create_room("OFFICE", "Hogwarts")
        offices = self.amity.offices
        expected = "Office Successfully Created"
        self.assertEqual(room_msg, expected)
        # assert that Hogwarts is in the offices list
        self.assertTrue(any(office.name == "Hogwarts" for office in offices))

    def test_living_space_created(self):
        """ test whether living room is created """
        room_msg = self.amity.create_room("LIVINGSPACE", "Php")
        living_spaces = self.amity.living_spaces
        expected = "Living Space Successfully Created"
        self.assertEqual(room_msg, expected)
        self.assertTrue(
            any(living_space.name == "Php" for living_space in living_spaces))

    def test_add_person(self):
        """ test whether person has been successfully added """
        all_people = self.amity.fellows + self.amity.staff
        fellow = self.amity.add_person("Omar", "FELLOW", "Y")
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
        pass

    def test_reallocation_fails_if_room_doesnt_exist(self):
        """ Cannot reallocate to a non-existent room """
        res = self.amity.reallocate_person("chuchu@chuchu", "The_Tsavo")
        self.assertEqual(res, "The room The_Tsavo does not exist!")

    def test_print_allocations(self):
        """ Print people and the rooms they have been allocated """
        pass

    def test_print_unallocated(self):
        """ Print a list of people who have not been allocated a room"""
        pass

    def test_save_allocations_to_file(self):
        """ Save people and the rooms they have been allocated to file"""
        pass
