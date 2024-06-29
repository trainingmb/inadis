#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
import models
from models.base_model import BaseModel
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes


classes = {"Creator": Creator, "Creation": Creation,
          "Post": Post, "PostContent": PostContent, "User": User}
fields = {"Creator": [['reference','int','Integer Reference for the Creator'],
                      ['name', 'str', 'Name of the Creator'],
                      ['link', 'str', 'Link to the Creators Page']],
          "Creation": [['creator_id', 'str', 'ID of the Creator'],
                       ['regexfilter', 'str', 'Filter for the titles of the Posts'],
                       ['name', 'str', 'Name of the Creation']],
          "Post": [['creation_id','str','ID of the Creation'],
                   ['title', 'str', 'Title of the Post'],
                   ['comment', 'str', 'A comment on the post'],
                   ['reference','int','Integer Reference for the Post'],
                   ['posted_at', 'datetime', 'Timestamp of when the post was uploaded'],
                   ['fetched_at', 'datetime', 'Timestamp of when the post was fetched']],
          "PostContent": [['post_id', 'str', 'Unique Identifier for the relating post'],
                          ['content', 'str', 'Content of the post usually very large text']]
          "User": [['name', 'str', 'Name of the user'],
                   ['email', 'str', 'User Email'],
                   ['password', 'str', 'User password']]}

class HBNBCommand(cmd.Cmd):
    """ INADIS console """
    prompt = '(inadis) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_exit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                print(key, value)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_fields(self, arg):
        """Get Fields for a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            flds = fields[args[0]]
        else:
            print("** class doesn't exist **")
            return False
        for value in flds:
            print('{}<{}>:\n\t{}'.format(value[0],value[1],value[2]))

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", \n".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        integers = ["reference"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if True:
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()