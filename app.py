#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 This example uses docopt with the built in cmd module to demonstrate an
 interactive command application.

 Usage:
    Amity create_room <room_type> <room_names>...
    Amity add_person <f_name> <l_name> (Fellow|Staff) [<wants_accomodation>]
    Amity reallocate_person <name> <new_room_name>
    Amity allocate_unallocated
    Amity reallocate_person <person_identifier> <new_room_name>
    Amity load_people
    Amity print_allocations [-o=<filename>]
    Amity print_unallocated [-o=<filename>]
    Amity print_room <room_name>
    Amity save_state [--db=<database_name>]
    Amity load_state [--db=<database_name>]
    Amity (-i | --interactive)
    Amity (-h | --help)
    Amity (--version)

 Options:
    -i, --interactive   Interactive Mode
    -h, --help   Show this screen and exit
    --version   Show version and exit
    -o=filename    Specify output file
    --db=database_name Database to save session data
 """

import cmd
import os
import sys
import time

from docopt import docopt, DocoptExit
from pyfiglet import figlet_format, Figlet
from termcolor import cprint
from amity import Amity
from clint.textui import colored, indent, puts


def docopt_cmd(func):
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg, version='Amity 1.0')

        except DocoptExit as error:

            # The DocoptExit is thrown when the args do not match
            # We print a message to the user and the usage block
            puts(colored.red("Invalid Command!"))
            print(error)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)

    return fn


def launch():
    time.sleep(2)
    with indent(84):
        puts(colored.magenta(figlet_format('Amity SP', font='sub-zero')))
    time.sleep(1)
    with indent(60):
        puts(
            colored.cyan("Welcome to the Amity Space Allocator." +
                         "Here is a list of commands for your use " +
                         "Type 'help' anytime to access available commands"))
    with indent(84):
        puts(colored.blue(__doc__))


class AppAmity(cmd.Cmd):
    launch()
    prompt = (colored.magenta('\n  ⚡  '))
    file = None
    Amity = Amity()

    @docopt_cmd
    def do_create_room(self, args):
        """ Usage: create_room <room_type> <room_names>..."""
        room_type = args["<room_type>"]
        room_names = args["<room_names>"]

        for room in room_names:
            try:
                self.Amity.create_room(room_type, room)
            except:
                print("Something went wrong.")

    @docopt_cmd
    def do_add_person(self, args):
        """ Usage: add_person <f_name> <l_name> <role> [<wants_accomodation>] """
        try:
            if args["<role>"] == "Fellow":
                role = "FELLOW"
            else:
                role = "STAFF"

            self.Amity.add_person(args['<f_name>'], args['<l_name>'], role,
                                  args['<wants_accomodation>'])
        except Exception as e:
            print(e.args)

    @docopt_cmd
    def do_reallocate_person(self, args):
        """ Usage: reallocate_person <f_name> <l_name> <new_room_name> """

        print(
            self.Amity.reallocate_person(args["<f_name>"], args["<l_name>"],
                                         args["<new_room_name>"]))

    @docopt_cmd
    def do_load_people(self, args):
        """ Usage: load_people <filename>"""

        self.Amity.load_people(args["<filename>"])

    @docopt_cmd
    def do_print_allocations(self, args):
        """ Usage: print_allocations [--o=filename] """

        filename = args["--o"]

        self.Amity.print_allocations(filename)
        # if not args["-o"]:
        #     self.Amity.print_allocations()

        # elif args["-o"] != None:
        #     # args["-o"] = "allocations"
        #     self.Amity.print_allocations(args["-o"])

    @docopt_cmd
    def do_print_unallocated(self, args):
        """ Usage: print_unallocated [-o=<filename>] """

        if not args["-o"]:
            self.Amity.print_unallocated()

        elif args["-o"] != None:
            self.Amity.print_unallocated(args["-o"])

    @docopt_cmd
    def do_print_room(self, args):
        """ Usage: print_room <room_name> """

        self.Amity.print_room(args["<room_name>"])

    @docopt_cmd
    def do_save_state(self, args):
        """ Usage: save_state [--db=<database_name>] """
        if not args["--db"]:
            args["--db"] = "amity_db"

        self.Amity.save_state(args["--db"])

    @docopt_cmd
    def do_load_state(self, args):
        """ Usage: load_state <database_name> """

        self.Amity.load_state(args["<database_name>"])

    def do_quit(self, args):
        """ Quits out of Interactive Mode """
        print("Exiting Application. Catch you later!")

        exit()


if __name__ == "__main__":
    try:
        AppAmity().cmdloop()
    except KeyboardInterrupt:
        print("Exiting Application. Catch you later!")
