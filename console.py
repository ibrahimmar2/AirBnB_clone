#!/usr/bin/python
"""
Module for console
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def split_curly_braces(e_arg):
    """
    Splits the curly braces for the update method
    """
    CurlyBraces = re.search(r"\{(.*?)\}", e_arg)

    if CurlyBraces:
        Id_With_Comma = shlex.split(e_arg[:CurlyBraces.span()[0]])
        id = [i.strip(",") for i in Id_With_Comma][0]

        str_data = CurlyBraces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return id, arg_dict
    else:
        Command = e_arg.split(",")
        if Command:
            try:
                id = Command[0]
            except Exception:
                return "", ""
            try:
                Attr_Name = Command[1]
            except Exception:
                return id, ""
            try:
                attr_value = Command[2]
            except Exception:
                return id, Attr_Name
            return f"{id}", f"{Attr_Name} {attr_value}"


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    Valid_Classes = ["BaseModel", "User", "Amenity",
                     "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_EOF(self, arg):
        """
        EOF (Ctrl+D) signal to exit the program.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name>
        """
        Command = shlex.split(arg)

        if len(Command) == 0:
            print("** class name missing **")
        elif Command[0] not in self.Valid_Classes:
            print("** class doesn't exist **")
        else:
            New_Instance = eval(f"{Command[0]}()")
            storage.save()
            print(New_Instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        Command = shlex.split(arg)

        if len(Command) == 0:
            print("** class name missing **")
        elif Command[0] not in self.Valid_Classes:
            print("** class doesn't exist **")
        elif len(Command) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            k = "{}.{}".format(Command[0], Command[1])
            if k in objects:
                print(objects[k])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        Command = shlex.split(arg)

        if len(Command) == 0:
            print("** class name missing **")
        elif Command[0] not in self.Valid_Classes:
            print("** class doesn't exist **")
        elif len(Command) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(Command[0], Command[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: <User>.all()
                <User>.show()
        """
        objects = storage.all()

        Command = shlex.split(arg)

        if len(Command) == 0:
            for key, value in objects.items():
                print(str(value))
        elif Command[0] not in self.Valid_Classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == Command[0]:
                    print(str(value))

    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class
        usage: <class name>.count()
        """
        objects = storage.all()

        Command = shlex.split(arg)

        if arg:
            cls_nm = Command[0]

        count = 0

        if Command:
            if cls_nm in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == cls_nm:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        Command = shlex.split(arg)

        if len(Command) == 0:
            print("** class name missing **")
        elif Command[0] not in self.Valid_Classes:
            print("** class doesn't exist **")
        elif len(Command) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(Command[0], Command[1])
            if key not in objects:
                print("** no instance found **")
            elif len(Command) < 3:
                print("** attribute name missing **")
            elif len(Command) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                Curly_Braces = re.search(r"\{(.*?)\}", arg)

                if Curly_Braces:
                    try:
                        str_data = Curly_Braces.group(1)

                        arg_dict = ast.literal_eval("{" + str_data + "}")

                        attribute_names = list(arg_dict.keys())
                        attribute_values = list(arg_dict.values())
                        try:
                            attr_name1 = attribute_names[0]
                            attr_value1 = attribute_values[0]
                            setattr(obj, attr_name1, attr_value1)
                        except Exception:
                            pass
                        try:
                            attr_name2 = attribute_names[1]
                            attr_value2 = attribute_values[1]
                            setattr(obj, attr_name2, attr_value2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:

                    attr_name = Command[2]
                    attr_value = Command[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()

    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        """
        arg_list = arg.split('.')

        cls_nm = arg_list[0]  # incoming class name

        command = arg_list[1].split('(')

        cmd_met = command[0]  # incoming command method

        e_arg = command[1].split(')')[0]  # extra arguments

        method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
                }

        if cmd_met in method_dict.keys():
            if cmd_met != "update":
                return method_dict[cmd_met]("{} {}".format(cls_nm, e_arg))
            else:
                if not cls_nm:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = split_curly_braces(e_arg)
                except Exception:
                    pass
                try:
                    call = method_dict[cmd_met]
                    return call("{} {} {}".format(cls_nm, obj_id, arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
