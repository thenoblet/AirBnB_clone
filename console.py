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


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand - AirBnB command line interface (CLI).

    This class implements a command-line interface (CLI) for an AirBnB clone
    application. It allows users to interact with the application by
    entering commands through the console.

    Attributes:
    - prompt (str): Custom prompt for the command-line interface.

    Methods:
    do_quit(self, args): Command that exits or quits the console.
    help_quit(self): Provides information about the quit command.
    do_EOF(self, args): Command that exits the console (Ctrl+D).
    help_EOF(self): Provides information about the EOF command.
    emptyline(self): Upon encountering blank line + `Enter` key, does nothing.
    precmd(self, line): Preprocesses each command line before execution.
    do_help(self, args): Custom handling for the help command.
    """
    prompt = '(hbnb) '

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

    def precmd(self, line):
        """
        Preprocesses each command line before execution.

        Converts the command to lowercase it is a valid command but not 'EOF',
        converts it to uppercase if the command is the 'EOF' command whatever
        letter case regardless.
        """
        if line.strip().lower() != 'eof':
            return line.lower()
        else:
            return line.upper()

    def do_help(self, args):
        """
        This method provides custom handling for the help command. If the
        argument is 'EOF', it displays help information specific to the 'EOF'
        command using the `help_EOF` method. Otherwise, it delegates to the
        base class's `do_help` method after converting the argument to
        lowercase.
        """
        if args.upper() == "EOF":
            self.help_EOF()
        else:
            super().do_help(args.lower())


if __name__ == '__main__':
    HBNBCommand().cmdloop()
