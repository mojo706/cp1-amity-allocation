""" Contains tests for the main amity class and most of it's functions"""
import unittest
import os
from amity_functions import Amity



class TestAmity(unittest.TestCase):
    """ Class that contains test for the funtions defined in amity.py """

    def setUp(self):
        self.amity_test = Amity()

    def test_input_is_string(self):
        """ test whether the input is a string or not"""

        self.assertEqual(self.amity_test.create_room(
            2, "Tsavo"), "Invalid Input", msg="Invalid Input")

    def test_office_created(self):
        """ test if office is successfully created"""
        offices = len(self.amity_test.offices)

        assert (len(self.amity_test.offices), offices+1)

    def test_living_space_created(self):
        """ test whether living room is created """
        living_spaces = len(Amity.living_spaces)

        assert (len(self.amity_test.living_spaces, living_spaces + 1))

    def test_if_room_exists(self):
        """ test whether room already exists"""

        self.assertIn("Hogwarts", self.amity_test.all_rooms)

    def test_add_person(self):
        """ test whether person can be added to a room """
        all_people=len(Amity.all_people)

        self.assertEqual(len(Amity.all_people), all_people + 1)

    def test_allocate_person_to_room(self):
       """ Allocate a person an office or living space """

    def test_adding_fellow(self):
        """ Is the fellow added successfully"""

    def test_adding_staff(self):
        """ Is the staff added successfully"""
        initial_staff_count = len(self.Amity.all_staff)

        new_staff_count = len(self.Amity.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1, msg="Failed to add new staff")
    def test_reallocate_person(self):
        """ Move a person from one office space or living space to another"""

    def test_reallocation_fails_if_room_doesnt_exist(self):
        """ Cannot reallocate to a non-existent room """
        res = self.amity_test.reallocate_person("chuchu@chuchu", "The_Tsavo")
        self.assertEqual(res, "The room The_Tsavo does not exist!")

    def test_print_allocations(self):
        """ Print people and the rooms they have been allocated """


    def test_print_unallocated(self):
        """ Print a list of people who have not been allocated a room"""

    def test_save_allocations_to_file(self):
        """ Save people and the rooms they have been allocated to file"""
