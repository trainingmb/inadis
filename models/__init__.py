#!/usr/bin/python3
"""
Initialize Models Package
"""

from os import getenv, environ

storage_t = getenv("INADIS_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.mysqldb_storage import MySQLDBStorage
    print("Working ON MySQLDB Storage")
    storage = MySQLDBStorage()
elif True:
    storage_t = 'db'
    from models.engine.sqlitedb_storage import SQLiteDBStorage
    print("Working ON SQLiteDB Storage")
    storage = SQLiteDBStorage()
else:
    from models.engine.file_storage import FileStorage
    print("Working ON File Storage")
    storage = FileStorage()
storage.reload()