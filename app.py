"""
 This example uses docopt with the built in cmd module to demonstrate an
 interactive command application.
 Usage:
    Amity create_room (Office|Living-Space|Space)<room_name>...
    Amity list_rooms
    Amity delete_room <room_identifier>
    Amity add_person <person_name> <person_gender> (Fellow|Staff) [<wants_accommodation>]
    Amity list_people
    Amity delete_person <person_identifier>
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
    -h, --help Show on this screen and then exit
    --version   Show version and exit
    -o=filename    Specify output file
    --db=database_name Database to save session data
 """
import cmd
import os
import sys

from docopt import docopt, DocoptExit
from amity import Amity


def docopt_cmd(func):
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg, version='Amity 1.0')

        except DocoptExit as error:

            # The DocoptExit is thrown when the args do not match
            # We print a message to the user and the usage block
            print("Invalid Command!")
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


class AppAmity(cmd.Cmd):
    
    def intro():
        print ('It works')
    
    introduction = intro()
    prompt = 'Amity->>>'
    file = None

    def do_help(self, args):
        pass

    @docopt_cmd
    def do_create_room(self, args):
        """ Usage: create_room <room_type> <room_names>..."""


        if args['room_type'].uppper() == "OFFICE":
            room_type = "OFFICE"
        elif args['room_type'].uppper() == "LIVING SPACE":
            room_type = "LIVING SPACE"
        else:
            room_type = args['room_type'].uppper()
        
        Amity.create_room(self, room_type, args['<room_names>'])
    
    @docopt_cmd
    def do_add_person(self, args):
        """ Usage: add_person <f_name> <l_name> (Fellow|Staff) [<wants_accomodation>] """
        print(args)

        if args['Fellow']:
            role = "FELLOW"
        else:
            role = "STAFF"
        
        Amity.add_person(args['<f_name>'], args['<l_name>'], role, args['<wants_accomodation>'])

    @docopt_cmd
    def do_reallocate_person

if __name__ == "__main__":
    try:
        AppAmity().cmdloop()
    except KeyboardInterrupt:
        print("Exiting Application. Catch you later!")