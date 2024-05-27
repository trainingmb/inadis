#!/usr/bin/python3
"""
Contains the class MySQLDBStorage
"""

from models.engine.db_storage import Base, create_engine, DBStorage, getenv 

class MySQLDBStorage(DBStorage):
    """interacts with the SQLite database"""

    def __init__(self):
        """Instantiate a DBStorage object"""
        INADIS_MYSQL_USER = getenv('INADIS_MYSQL_USER')
        INADIS_MYSQL_PWD = getenv('INADIS_MYSQL_PWD')
        INADIS_MYSQL_HOST = getenv('INADIS_MYSQL_HOST')
        INADIS_MYSQL_DB = getenv('INADIS_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(INADIS_MYSQL_USER,
                                             INADIS_MYSQL_PWD,
                                             INADIS_MYSQL_HOST,
                                             INADIS_MYSQL_DB))
        Base.metadata.bind = self.__engine
        super().__init__(self.__engine)