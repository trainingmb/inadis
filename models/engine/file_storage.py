#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import models
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from hashlib import md5

classes = {"Creator": Creator, "Creation": Creation,
          "Post": Post, "PostContent":PostContent}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict(save_fs=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)
    
    def all_defer(self, cls, deffered):
        """query on the current database session"""
        new_dict = {}
        for key, value in self.__objects.items():
            if cls == value.__class__ or cls == value.__class__.__name__:
                value.pop(deffered, None)
                new_dict[key] = value
        return (new_dict)
    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def filtered_get(self, cls, **kwargs):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        filtered_results = []
        for value in all_cls.values():
            obj_flag = False
            for key, v in kwargs.items():
                try:
                    x = getattr(value, key, None)
                    if x is not None and x == v:
                        obj_flag=True
                    else:
                        obj_flag=False
                except Exception as e:
                    obj_flag=False
                if obj_flag == False:
                    break
            if obj_flag == True:
                filtered_results.append(value)
        if (len(filtered_results) < 1):
            return None
        return filtered_results 

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count