#!/usr/bin/python3

""""
Module: console

Description:
This is a module contains the HBNBCommand class which implements a command-line
interface (CLI) for an AirBnB clone application. The CLI allows users to
interact with the application by entering commands through the console.

Usage:
To use this module, execute the script directly. The script will invoke a
command-line interface with the prompt '(hbnb)'. Enter commands to
interact with the application. For each command use, `help` will display
the neccessary information about it.

Example:
example@user:/AirBnB_clone$ ./console.py
(hbnb)
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) help quit
Quit command to exit the console

(hbnb)
(hbnb) quit
example@user:/AirBnB_clone$
"""

import cmd
import json
import shlex
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand - AirBnB command line interface (CLI).

    This class implements a command-line interface (CLI) for an AirBnB clone
    application. It allows users to interact with the application by
    entering commands through the console.

    Attributes:
    - prompt (str): Custom prompt for the command-line interface.
    - class_mapping (dict): Dictionary mapping class names to their
    corresponding classes.

    Methods:
    do_quit(self, args): Command that exits or quits the console.
    help_quit(self): Provides information about the quit command.
    do_EOF(self, args): Command that exits the console (Ctrl+D).
    help_EOF(self): Provides information about the EOF command.
    emptyline(self): Upon encountering blank line + `Enter` key, does nothing.
    precmd(self, line): Preprocesses each command line before execution.
    do_help(self, args): Custom handling for the help command.
    help_help(self): Provides information about the help command.
    do_create(self, args): Creates a new instance of a specified class.
    help_create(self): Provides information about the create command.
    do_show(self, args): Prints the string representation of an instance
    based on the class name and id.
    help_show(self): Provides information about eht show command.
    do_destroy(self, args): Deletes an instance based on class name and id.
    (save the change into the JSON file).
    help_destroy(self): Provides information about the destroy command.
    do_all(self, args): Prints all string representation of all instances based
    or not on the class name.
    help_all(self): Provides information about the all command.
    do_update(self, args): Updates an instance based on the class name and id.
    help_update(self): Displays information about the update command.
    """

    prompt = ("(hbnb) ")
    class_mapping = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review,
            }

    def do_quit(self, args):
        '''
            Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
            Create a new instance of class BaseModel and saves it
            to the JSON file.
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = shlex.split(args)
            new_instance = eval(args[0])()
            new_instance.save()
            print(new_instance.id)

        except NameError:
            print("** class doesn't exist **")

    def help_create(self):
        """
        Provides information about the create command.
        """
        print("Creates a new instance of a specified class.\n")
        print("Usage: create <class_name>\n")

    def do_show(self, args):
        '''
            Print the string representation of an instance baed on
            the class name and id given as args.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        storage = FileStorage()
        storage.reload()
        obj_dict = storage.all()
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """
        Provides information about the show command.
        """
        print("Prints the string representation of an instance based on the\
class name and id.\n")
        print("Usage: show <class_name> <instance_id>\n")

    def do_destroy(self, args):
        '''
            Deletes an instance based on the class name and id.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        class_name = args[0]
        class_id = args[1]
        storage = FileStorage()
        storage.reload()
        obj_dict = storage.all()
        try:
            eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            del obj_dict[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def help_destroy(self):
        """
        Provides information about the destroy command.
        """
        print("Deletes an instance based on the class name and id.\n")
        print("Usage: destroy <class_name> <instance_id>\n")

    def do_all(self, args):
        """
        Prints all string representation of all instances based or not on the
        class name.

        Usage: all <class_name>
        """
        objects = storage.all()
        if not args:
            print([str(obj) for obj in objects.values()])
            return

        class_name = args.split()[0]
        if class_name not in self.class_mapping:
            print('** class doesn\'t exist **')
            return

        print([str(obj) for key, obj in objects.items() if key.split('.')[0]
              == class_name])

    def help_all(self):
        """
        Provides information about the all command.
        """
        print("Prints all string representation of all instances based or not\
on the class name.\n")
        print("Usage: all <class_name>\n")

    def do_update(self, args):
        """
        Updates an instance attribute based on class name and id.

        Usage: update <class_name> <instance_id> <attribute_name>
        "<attribute_value>"

        This command updates an attribute of an instance specified by its class
        name and id. It requires the class name, instance id, attribute name,
        and the new attribute value enclosed in double quotes.
        - If class name or instance id is missing, prints respective error
        message.
        - If the instance for the class name and instance id doesn't exist,
        prints an error message.
        - If the attribute name or value is missing, prints respective
        error message.
        - Only simple arguments (string, integer, float) can be updated.
        - Attributes 'id', 'created_at', and 'updated_at' cannot be updated.
        """
        storage = FileStorage()
        storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def help_update(self):
        """
        Provides information about the update command.
        Usage: update <class name> <id> <attribute name> "<attribute value>"

        - Updates an instance attribute based on class name and id.
        - Only one attribute can be updated at a time.
        - The attribute name must be valid for the model.
        - The attribute value must be of the correct type.
        - If class name or id is missing, prints respective error message.
        - If instance for class name and id doesn't exist, prints error
        message.
        - If attribute name or value is missing, prints respective error
        message.
        - Only simple arguments (string, integer, float) can be updated.
        - id, created_at, and updated_at cannot be updated.
        """
        print("Updates an instance's attribute based on class name and id.\n\
\nUsage: update <class name> <id> <attribute name> <attribute value>.\n")

    def emptyline(self):
        '''
            Prevents printing anything when an empty line is passed.
        '''
        pass

    def do_count(self, args):
        '''
            Counts/retrieves the number of instances.
        '''
        obj_list = []
        storage = FileStorage()
        storage.reload()
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)
        print(len(obj_list))

    def default(self, args):
        '''
            Catches all the function names that are not expicitly defined.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except KeyError:
            print("*** Unknown syntax:", args[0])


if __name__ == "__main__":
    '''
        Entry point for the loop.
    '''
    HBNBCommand().cmdloop()
