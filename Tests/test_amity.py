""" Contains tests for the main amity class and most of it's functions"""
import unittest
import os
from amity import Amity


class TestAmity(unittest.TestCase):
    """ Class that contains test for the funtions defined in amity.py """

    def setUp(self):
        self.amity = Amity()
        # self.amity.create_room("OFFICE", "Addis")
        # self.amity.create_room("OFFICE", "Accra")
        # self.amity.create_room("LIVINGSPACE", "Camelot")

    def test_input_can_only_be_string(self):
        """ test whether the input is a string or not"""
        # Test wrong room type
        with self.assertRaises(ValueError):
            self.amity.create_room(2, "Tsavo")

        # Test wrong room name
        with self.assertRaises(ValueError):
            self.amity.create_room("Office", {})

    def test_existing_room_name(self):
        self.amity.create_room("OFFICE", ["Accra"])
        room_msg = self.amity.create_room("OFFICE", ["Accra"])
        expected = "The room Accra has already been created"
        self.assertEqual(room_msg, expected)

    def test_office_created(self):
        """ test if office is successfully created"""
        room_msg = self.amity.create_room("OFFICE", ["Hogwarts"])
        offices = self.amity.offices
        expected = "Office Successfully Created"
        self.assertEqual(room_msg, expected)
        # assert that Hogwarts is in the offices list
        self.assertTrue(
            any(office.room_name == "Hogwarts" for office in offices))

    def test_living_space_created(self):
        """ test whether living room is created """
        room_msg = self.amity.create_room("LIVINGSPACE", ["Php"])
        living_spaces = self.amity.living_spaces
        expected = "Living Space Successfully Created"
        self.assertEqual(room_msg, expected)
        self.assertTrue(
            any(living_space.room_name == "Php" for living_space in living_spaces))

    def test_adding_fellow(self):
        """ test whether person has been successfully added """
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("OFFICE", "Addis")
        all_fellows = self.amity.fellows
        success_msg = self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        expected_output = "The fellow OMAR EUGENE has been successfully added and allocated the office Addis and the living space Valhala"
        self.assertEqual(success_msg, expected_output)
        self.assertTrue(
            any(fellow.name == "OMAR EUGENE" for fellow in all_fellows))

    def test_adding_staff(self):
        """ Is the staff added successfully"""
        self.amity.create_room("OFFICE", "Addis")
        all_staff = self.amity.staff
        staff = self.amity.add_person("Kosy", "STAFF")
        expected_output = "The staff member KOSY has been successfully added and allocated the office Addis"
        self.assertEqual(staff, expected_output)
        self.assertTrue(any(staff.name == "KOSY" for staff in all_staff))

    def test_reallocate_person(self):
        """ Move a person from one office space or living space to another"""
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("OFFICE", "Addis")
        staff = self.amity.add_person("Kosy", "STAFF")
        self.amity.create_room("OFFICE", "Accra")
        reallocated = self.amity.reallocate_person("Kosy", "Accra")
        expected_output = "KOSY has been successfully reallocated to Accra"
        self.assertEqual(reallocated, expected_output)

    def test_reallocation_fails_if_room_doesnt_exist(self):
        """ Cannot reallocate to a non-existent room """
        # res = self.amity.reallocate_person("chuchu@chuchu", "The_Tsavo")
        # self.assertEqual(res, "The room The_Tsavo does not exist!")
        pass

    def test_print_room(self):
        """ Test Print Room """
        self.amity.create_room("OFFICE", "Addis")
        self.amity.add_person("Kosy", "Kironde", "STAFF")
        self.amity.add_person("Janoosh", "Ebrahim", "FELLOW")
        self.amity.add_person("Chuchu", "Omar", "FELLOW")
        printed = self.amity.print_room("Addis")
        self.assertTrue(
            ("KOSY KIRONDE" and "JANOOSH EBRAHIM" and "CHUCHU OMAR") in printed.upper())

    def test_print_allocations(self):
        """ Print people and the rooms they have been allocated """
        pass

    def test_print_unallocated_saves_to_filename(self):
        """ Print a list of people who have not been allocated a room"""
        self.amity.create_room("OFFICE", "Addis")
        self.amity.add_person("Kosy", "Kironde", "STAFF")
        self.amity.add_person("Janoosh", "Ebrahim", "FELLOW")
        self.amity.add_person("Munyi", "Jonathan", "FELLOW")
        self.amity.add_person("Tina", "Murimi", "FELLOW")
        self.amity.add_person("Joe", "Nzau", "FELLOW")
        self.amity.add_person("Ahmed", "Yusuf", "FELLOW")
        self.amity.add_person("Alex", "Ngugi", "FELLOW")
        self.amity.add_person("Jonathan", "Kamau", "FELLOW")
        self.amity.add_person("Paul", "Upendo", "FELLOW")
        self.amity.add_person("Dj", "Mulobi", "FELLOW")
        unallocated = self.amity.print_unallocated("test")
        expected_output = "\033[1m \nData has been successfully saved to test.txt\n \033[0m"
        self.assertEqual(unallocated, expected_output)           


    def test_save_allocations_to_file(self):
        """ Save people and the rooms they have been allocated to file"""
        pass

    def test_save_state(self):
        """ Tests whether the current state of the app has been saved to a database """
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("OFFICE", "Addis")
        self.amity.add_person("Kosy", "DThree", "STAFF")
        self.amity.create_room("OFFICE", "Accra")
        self.amity.add_person("Janoosh", "Janoosh", "FELLOW", "Y")
        success_msg = self.amity.save_state("test")
        expected_msg = "State Saved Successfully"
        self.assertEqual(success_msg, expected_msg)
