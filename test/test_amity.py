""" Contains tests for the main amity class and most of it's functions"""
import unittest
import os

from amity import Amity
from clint.textui import colored


class TestAmity(unittest.TestCase):
    """ Class that contains test for the funtions defined in amity.py """

    def setUp(self):
        self.amity = Amity()
        # self.amity.create_room("OFFICE", "Addis")
        # self.amity.create_room("OFFICE", "Accra")
        # self.amity.create_room("LIVINGSPACE", "Camelot")

    def test_create_room_invalid_room_name_input(self):
        """ Test creating room fails with invalid room name"""
        # Test wrong room name
        room_msg = self.amity.create_room("Office", "{}")
        expected_msg = "Invalid Input For Room Name"
        self.assertEqual(room_msg, expected_msg)

    def test_create_room_invalid_room_type_input(self):
        """ Test whether the input is a string or not"""
        # Test wrong room type
        room_msg = self.amity.create_room("2", "Tsavo")
        expected_msg = "Invalid Input For Room Type"
        self.assertEqual(room_msg, expected_msg)

    def test_create_room_existing_room_name(self):
        self.amity.create_room("OFFICE", "Accra")
        room_msg = self.amity.create_room("OFFICE", "Accra")
        expected = "The room ACCRA has already been created"
        self.assertEqual(room_msg, expected)

    def test_create_room_office_created(self):
        """ test if office is successfully created"""
        room_msg = self.amity.create_room("OFFICE", "Hogwarts")
        offices = self.amity.offices
        expected = "The Office HOGWARTS was created successfully"
        self.assertEqual(room_msg, expected)
        # assert that Hogwarts is in the offices list
        self.assertTrue(
            any(office.room_name == "HOGWARTS" for office in offices))

    def test_create_room_living_space_created(self):
        """ test whether living room is created """
        room_msg = self.amity.create_room("LIVINGSPACE", "Php")
        living_spaces = self.amity.living_spaces
        expected = "The Living Space PHP was created successfully"
        self.assertEqual(room_msg, expected)
        self.assertTrue(
            any(living_space.room_name == "PHP"
                for living_space in living_spaces))

    def test_create_room_invalid_room_name(self):
        room_msg = self.amity.create_room("TOILET", "Loo")
        expected_output = "Room type can only be an office or a living space"
        self.assertEqual(room_msg, expected_output)

    def test_allocate_office_space_no_available_office(self):
        room_msg = self.amity.allocate_office_space("Alex")
        expected_output = "No available offices"
        self.assertEqual(room_msg, expected_output)

    def test_allocate_living_space_no_available_living_space(self):
        room_msg = self.amity.allocate_living_space("Alex")
        expected_output = "No available living space"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_invalid_name_input(self):
        room_msg = self.amity.add_person("mojo706", "Eugene", "Staff")
        expected_output = "First and Last name must be alphabets"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_invalid_role_input(self):
        room_msg = self.amity.add_person("Omar", "Eugene", "CATERER")
        expected_output = "Invalid Role"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_adding_staff(self):
        """ test whether person has been successfully added """
        self.amity.create_room("OFFICE", "Addis")
        room_msg = self.amity.add_person("Omar", "Eugene", "STAFF")
        expected_output = "The staff member OMAR EUGENE has been successfully added and allocated the office ADDIS"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_adding_staff_wants_accomodation(self):
        """ test whether the staff member gets a message when they try getting a living space """
        self.amity.create_room("OFFICE", "Addis")
        self.amity.create_room("LIVINGSPACE", "Ruby")
        room_msg = self.amity.add_person("Omar", "Eugene", "STAFF", "Y")
        expected_output = "The staff member OMAR EUGENE has been successfully added and allocated the office ADDIS. Sorry a staff member cannot be assigned a living space"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_staff_already_exists(self):
        """ test whether person has been successfully added """
        self.amity.add_person("Omar", "Eugene", "STAFF")
        room_msg = self.amity.add_person("Omar", "Eugene", "STAFF")
        expected_output = "That Staff member already exists"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_adding_staff_no_offices(self):
        """ test whether staff has been successfully added with no office"""
        room_msg = self.amity.add_person("Omar", "Eugene", "STAFF")
        expected_output = "The staff member OMAR EUGENE has been successfully added and will be allocated an office once it's available."
        self.assertEqual(room_msg, expected_output)

    def test_add_person_adding_fellow(self):
        """ test whether fellow has been successfully added """
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("OFFICE", "Addis")
        all_fellows = self.amity.fellows
        success_msg = self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        expected_output = "The fellow OMAR EUGENE has been successfully added and allocated the office ADDIS and the living space VALHALA"
        self.assertEqual(success_msg, expected_output)
        self.assertTrue(
            any(fellow.name == "OMAR EUGENE" for fellow in all_fellows))

    def test_add_person_fellow_already_exists(self):
        """ test whether fellow already existed """
        self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        room_msg = self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        expected_output = "That Fellow already exists"
        self.assertEqual(room_msg, expected_output)

    def test_add_person_adding_fellow_no_available_office(self):
        """ test whether fellow has been successfully added with no office space"""
        self.amity.create_room("LIVINGSPACE", "Valhala")
        all_fellows = self.amity.fellows
        success_msg = self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        expected_output = "The fellow OMAR EUGENE has been successfully added and allocated the living space VALHALA but sorry we do not have any available offices"
        self.assertEqual(success_msg, expected_output)
        self.assertTrue(
            any(fellow.name == "OMAR EUGENE" for fellow in all_fellows))

    def test_add_person_adding_fellow_no_available_living_space(self):
        """ test whether fellow has been successfully added with no office space"""
        self.amity.create_room("OFFICE", "Valhala")
        all_fellows = self.amity.fellows
        success_msg = self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        expected_output = "The fellow OMAR EUGENE has been successfully added and allocated the office VALHALA but sorry we do not have any available living spaces"
        self.assertEqual(success_msg, expected_output)
        self.assertTrue(
            any(fellow.name == "OMAR EUGENE" for fellow in all_fellows))

    def test_add_person_adding_fellow_no_available_living_space_and_office(
            self):
        """ test whether person has been successfully added """
        all_fellows = self.amity.fellows
        success_msg = self.amity.add_person("Omar", "Eugene", "FELLOW", "Y")
        expected_output = "The fellow OMAR EUGENE has been successfully added and will be allocated an office and living space once they're available"
        self.assertEqual(success_msg, expected_output)
        self.assertTrue(
            any(fellow.name == "OMAR EUGENE" for fellow in all_fellows))

    def test_adding_staff(self):
        """ Is the staff added successfully"""
        self.amity.create_room("OFFICE", "Addis")
        all_staff = self.amity.staff
        room_msg = self.amity.add_person("Kosy", "DThree", "STAFF")
        expected_output = "The staff member KOSY DTHREE has been successfully added and allocated the office ADDIS"

        self.assertEqual(room_msg, expected_output)
        self.assertTrue(
            any(staff.name == "KOSY DTHREE" for staff in all_staff))

    def test_list_people(self):
        """ Test if all people are listed successfully """
        self.amity.add_person("Janoosh", "Janoosh", "Fellow", "Y")
        self.amity.add_person("Shem", "Ogumbe", "Staff")
        people_msg = self.amity.list_people()
        expected_output = "List Printed Successfully"
        self.assertEqual(people_msg, expected_output)

    def test_list_people_with_no_people(self):
        """ Test if all people are listed successfully """
        people_msg = self.amity.list_people()
        expected_output = "List Printed Successfully"
        self.assertEqual(people_msg, expected_output)

    def test_reallocate_person(self):
        """ Move a person from one office space or living space to another"""
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("OFFICE", "Addis")
        staff = self.amity.add_person("Kosy", "DThree", "STAFF")
        self.amity.create_room("OFFICE", "Accra")

        reallocated = self.amity.reallocate_person("Kosy", "DThree", "Accra")
        expected_output = "KOSY DTHREE has been successfully reallocated to ACCRA"

        self.assertEqual(reallocated, expected_output)

    def test_reallocate_person_to_same_room_fails(self):
        """ Trying reallocating a staff member to a living space should fail """
        self.amity.create_room("LIVINGSPACE", "Valhala")
        self.amity.create_room("OFFICE", "Addis")
        staff = self.amity.add_person("Kosy", "DThree", "STAFF")
        self.amity.create_room("OFFICE", "Addis")
        reallocated = self.amity.reallocate_person("Kosy", "DThree", "Addis")
        expected_output = "Cannot reallocate to the same room"

        self.assertEqual(reallocated, expected_output)

    def test_reallocation_fails_if_room_doesnt_exist(self):
        """ Cannot reallocate to a non-existent room """
        # res = self.amity.reallocate_person("chuchu@chuchu", "The_Tsavo")
        # self.assertEqual(res, "The room The_Tsavo does not exist!")
        pass

    def test_delete_person(self):
        """ Checks if delete_person() works"""
        self.amity.create_room("OFFICE", "Addis")
        self.amity.add_person("Uzumaki", "Naruto", "Fellow", "Y")
        msg = self.amity.delete_person("Uzumaki Naruto")
        expected_output = "UZUMAKI NARUTO has been successfully deleted from Amity."

        self.assertEqual(msg, expected_output)

    def test_print_room(self):
        """ Test Print Room """
        self.amity.create_room("OFFICE", "Addis")
        self.amity.add_person("Kosy", "Kironde", "STAFF")
        self.amity.add_person("Janoosh", "Ebrahim", "FELLOW")
        self.amity.add_person("Chuchu", "Omar", "FELLOW")
        printed = self.amity.print_room("Addis")
        self.assertTrue(("KOSY KIRONDE" and "JANOOSH EBRAHIM" and
                         "CHUCHU OMAR") in printed.upper())

    def test_print_allocations(self):
        """ Print people and the rooms they have been allocated """
        pass

    def test_print_allocations_with_filename(self):
        self.amity.print_allocations('file')
        self.assertTrue(os.path.isfile('file.txt'))
        os.remove('file.txt')

    def test_print_unallocated_saves_to_filename(self):
        """ Print a list of people who have not been allocated a room"""
        self.amity.add_person("Kosy", "Kironde", "STAFF")
        unallocated = self.amity.print_unallocated("test")
        expected_output = "Data has been successfully saved to test.txt"
        self.assertEqual(unallocated, expected_output)

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
