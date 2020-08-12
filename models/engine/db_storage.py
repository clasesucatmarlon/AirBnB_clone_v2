#!/usr/bin/python3
""" database storage class for AirBnB
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.city import City
from models.base_model import Base


class DBStorage:
    """ Class DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        """ Inicialize an instance of the class DBStorage """

        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB), pool_pre_ping=True)

        if HBNB_ENV == 'tets':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query session currenty of the database """
        
        dicc = {}
        if cls:
            for instance in self.__session.query(eval(cls)).all():
                dicc[instance.__class__.__name__ + '.' + str(instance.id)] = instance
        else:
            list_class = [User, State, City]
            for cla in list_class:
                for query_dic in self.__session.query(eval(cla)):
                    dicc[query_dic.__class__.__name__ + '.' + str(query_dic.id)] = query_dic
        return dicc
    
    def new(self, obj):
        """ Add object to actually database """
        self.__session.add(obj)
        
    def save(self):
        """ Commit all changes to actually database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deleted from actually database """
        self.__session.delete(obj)
        
    def reload(self):
        """ load storage """
        # Create table
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                           expire_on_commit=False)
        self.__session = scoped_session(session_factory)
