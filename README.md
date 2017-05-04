# cp1-amity-allocation
A Room allocation system for one of Andela's facilities called Amity.

## Installation
- Assuming you have **pip** install the following
```
>>  pip install virtualenv  

>> pip install virtualenvwrapper
```
We use `virtualenvwrapper` to manage more easily our virtual environments.

- Create a directory to hold your `virtualenvs`
```
>> mkdir ~/.virtualenvs
```

- Then add the following lines to the end of your **.bashrc** or **.zshrc** file
```
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```
- To activate the  settings above do the following
```
>> source .bashrc
```
- Create a new virtual environment using Python 3 with
```
>> mkvirtualenv --python=python3_path myenv
```
- While in your virtual environment clone the repo
```
>> git clone https://github.com/mojo706/cp1-amity-allocation
```
- Install the requirements using pip
```
>> pip install -r requirements.txt
```
- Run the app
```
>> python app.py -i
```
## Commands to run:

- Create a new office or living space run `create_room <room_type> <room_names>...`

- Add a new staff or fellow run `add_person <person_name> <role> [<wants_accomodation>]`. For fellows who want accomodation specify the optional "Y" parameter

- View all members in any room run `print_room <room_name>`

- View rooms and their occupants run `print_allocations [<filename>]` specifying a filename saves the records in a .txt file

- View all unallocated people run `print_unallocated [<filename>]` specifying a filename saves the records in a .txt file

- `load_people <filename>` loads people from an existing .txt file

- `reallocate_person <first_name> <last_name> <new_room_name>` reallocates a person from their current room to the given room

- `save_state [<database_name>]` saves the current state of the application to a database. Specifying the database_name saves the data to named database file

- `load_state <database_name>` loads data from an exisitng database  

- `list_people` lists all the people in Amity and their rooms  

- `delete_room <room_name>` removes the specified room from amity

- `delete_person <first_name> <last_name>` removes a person from amity 

- Run the tests **unittest**
```
>> python -m unittest discover -s test
```
- Get the test coverage
```
>> coverage run -m --source=. unittest discover -s test
>> coverage report -m
```
## Screenshots (if appropriate)
<img width="1678" alt="screenshot of amity space" src="https://cloud.githubusercontent.com/assets/908380/25542387/0feb8708-2c5b-11e7-9e61-5d6438131491.png">

## Project Demo Video
[![asciicast](https://asciinema.org/a/6r2qkx1eznas333goel7osad3.png)](https://asciinema.org/a/6r2qkx1eznas333goel7osad3)
