#!/usr/bin/env python3

import cmd
from models.base_model import BaseModel
from models import storage
import shlex
import re
import ast


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
        id_with_comma = shlex.split(e_arg[:CurlyBraces.span()[0]])
        id = [i.strip(",") for i in id_with_comma][0]

        str_data = CurlyBraces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return id, arg_dict
    else:
        comand = e_arg.split(",")
        if comand:
            try:
                id = comand[0]
            except Exception:
                return "", ""
            try:
                attr_name = comand[1]
            except Exception:
                return id, ""
            try:
                attr_value = comand[2]
            except Exception:
                return id, attr_name
            return f"{id}", f"{attr_name} {attr_value}"

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    
    valid_cls = ["BaseModel", "User", "Amenity", "Place",
                 "Review", "State", "City"]
    
    
    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_EOF(self, arg):
        """Exit the program when EOF (Ctrl+D) is reached"""
        print("")
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, arg):
        
        """
        Create a new instance of BaseModel, save it (to the JSON file) and print the id.
        Usage: create <class name>
        """
        
        comand = shlex.shlex(arg)
        
        if len(comand) == 0:
            print("** class name missing **")
        elif comand[0] not in self.valid_cls:
            print("** class doesn't exist **")
        else:
            NewInstance = BaseModel()
            NewInstance.save()
            print(NewInstance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        comand = shlex.split(arg)

        if len(comand) == 0:
            print("** class name missing **")
        elif comand[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(comand) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            k = "{}.{}".format(comand[0], comand[1])
            if k in objects:
                print(objects[k])
            else:
                print("** no instance found **")    


    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        comand = shlex.split(arg)

        if len(comand) == 0:
            print("** class name missing **")
        elif comand[0] not in self.valid_cls:
            print("** class doesn't exist **")
        elif len(comand) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(comand[0], comand[1])
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

        comand = shlex.split(arg)

        if len(comand) == 0:
            for key, value in objects.items():
                print(str(value))
        elif comand[0] not in self.valid_cls:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == comand[0]:
                    print(str(value))  



    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        comand = shlex.split(arg)

        if len(comand) == 0:
            print("** class name missing **")
        elif comand[0] not in self.valid_cls:
            print("** class doesn't exist **")
        elif len(comand) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(comand[0], comand[1])
            if key not in objects:
                print("** no instance found **")
            elif len(comand) < 3:
                print("** attribute name missing **")
            elif len(comand) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                CurlyBraces = re.search(r"\{(.*?)\}", arg)

                if CurlyBraces:
                    try:
                        StrData = CurlyBraces.group(1)

                        arg_dict = ast.literal_eval("{" + StrData + "}")

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

                    attr_name = comand[2]
                    attr_value = comand[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()


    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class
        usage: <class name>.count()
        """
        objects = storage.all()

        comand = shlex.split(arg)

        if arg:
            cls_nm = comand[0]

        count = 0

        if comand:
            if cls_nm in self.valid_cls:
                for obj in objects.values():
                    if obj.__class__.__name__ == cls_nm:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")


    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        """
        ArgList = arg.split('.')

        cls_nm = ArgList[0]  # incoming class name

        command = ArgList[1].split('(')

        CmdMet = command[0]  # incoming command method

        e_arg = command[1].split(')')[0]  # extra arguments

        MethodDict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
                }

        if CmdMet in MethodDict.keys():
            if CmdMet != "update":
                return MethodDict[CmdMet]("{} {}".format(cls_nm, e_arg))
            else:
                if not cls_nm:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = split_curly_braces(e_arg)
                except Exception:
                    pass
                try:
                    call = MethodDict[CmdMet]
                    return call("{} {} {}".format(cls_nm, obj_id, arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False



if __name__ == '__main__':
    HBNBCommand().cmdloop()
         
    