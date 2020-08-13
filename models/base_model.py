#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import datetime
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm
import models
from datetime import datetime
from sqlalchemy import Column, String, DateTime


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column('id', String(60), nullable=False, primary_key=True)

    created_at = Column(
        'created_at',
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    updated_at = Column(
        'updated_at',
        DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            """ storage.new(self) """
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            for ke, va in kwargs.items():
                setattr(self, ke, va)
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        my_dict = dict(self.__dict__)
        if "_sa_instance_state" in my_dict.keys():
            del my_dict["_sa_instance_state"]
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict["created_at"] = self.created_at.isoformat()
        return my_dict

        """Convert instance into dict format"""
        """dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary"""

    def delete(self):
        """ Delete instalncia from storage """
        models.storage.delete(self)
