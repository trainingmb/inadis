#!/usr/bin/python3
"""
Initialize Models Package
"""

from os import getenv, environ

storage_t = getenv("INADIS_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    print("Working ON DB Storage")
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    print("Working ON File Storage")
    storage = FileStorage()
storage.reload()