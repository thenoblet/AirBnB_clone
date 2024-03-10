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
import uuid
from models.base_model import BaseModel
from models import storage
from models import User
from models import State
from models import City
from models import Amenity
from models import Review


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
    prompt = '(hbnb) '
    class_mapping = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
            }

    def do_quit(self, args):
        """
        Quit command to exit the console.

        Usage: quit
        """
        return True

    def help_quit(self):
        """
        Provides information about the quit command.
        """
        print("Quit command to exit the console\n")

    def do_EOF(self, args):
        """
        End of file command (Ctrl+D) that exits the console.
        """
        print()
        return True

    def help_EOF(self):
        """
        Provides information about the EOF command
        """
        print("Press `Ctrl+D` to exit the console\n")

    def emptyline(self):
        """
        Upon encountering a blank line + `Enter`, do nothing
        """
        pass

    def help_help(self):
        """
        Provides information about the help command.

        This method explains the usage of the help command in the console.
        It informs users how to list available commands and how to obtain
        detailed help for a specific command using the 'help' command.

        """
        print("To list available commands, type 'help'.")
        print("\nTo get detailed help for a specific command, type 'help' \
followed by the command name.\n")

    def do_create(self, args):
        """
        Creates a new instance of a specified class.

        Usage: create <class_name>
        """
        if not args:
            print("** class name missing **")
            return

        class_name = args.split()[0]
        if class_name not in self.class_mapping:
            print('** class doesn\'t exist **')
            return
        new_instance = self.class_mapping[class_name]()
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """
        Provides information about the create command.
        """
        print("Creates a new instance of a specified class.\n")
        print("Usage: create <class_name>\n")

    def do_show(self, args):
        """
        Prints the string representation of an instance based on the class
        name and id.

        Usage: show <class_name> <instance_id>
        """
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        if args_list[0] not in self.class_mapping:
            print('** class doesn\'t exist **')
            return

        if len(args_list) == 1:
            print("** instance id missing **")
            return

        key = args_list[0] + "." + args_list[1]
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        print(objects[key])

    def help_show(self):
        """
        Provides information about the show command.
        """
        print("Prints the string representation of an instance based on the\
class name and id.\n")
        print("Usage: show <class_name> <instance_id>\n")

    def do_destroy(self, args):
        """
        Deletes an instance based on the class name and id.

        Usage: destroy <class_name> <instance_id>
        """
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        if args_list[0] not in self.class_mapping:
            print('** class doesn\'t exist **')
            return

        if len(args_list) == 1:
            print("** instance id missing **")
            return

        key = args_list[0] + "." + args_list[1]
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        del objects[key]
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
        arg = args.split()
        if not args:
            print("** class name missing **")
        elif arg[0] not in self.class_mapping:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        elif len(arg) < 3:
            print("** attribute name missing **")
        elif len(arg) < 4:
            print("** value missing **")
        else:
            _object = storage.all()
            key = "{}.{}".format(arg[0], arg[1])
            if key not in _object:
                print("** no instance found **")
                return
            instance = _object[key]
            setattr(instance, arg[2], arg[3])
            instance.save()

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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
