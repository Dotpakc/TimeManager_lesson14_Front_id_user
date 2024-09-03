import datetime
import random

from peewee import *

db = SqliteDatabase('company.sqlite3')

class BaseModel(Model):
    class Meta:
        database = db
        

class User(BaseModel):
    name = CharField()
    authorisation_code = CharField(default='1234', unique=True)
    
    def __str__(self):
        return self.name
    
    
class Session(BaseModel):
    user = ForeignKeyField(User, backref='sessions')
    active = BooleanField(default=True)
    start_time = DateTimeField( default=datetime.datetime.now )
    end_time = DateTimeField( null=True )

    
    def __str__(self):
        return f'{self.user} - {self.start_time} - {self.end_time}'


def create_tables():
    db.connect()
    db.create_tables([User, Session])
    db.close()
    

if __name__ == '__main__':
    create_tables()
    
    User.create(name='Alice', authorisation_code=random.randint(1000, 9999))
    User.create(name='Bob', authorisation_code=random.randint(1000, 9999))
    User.create(name='Charlie', authorisation_code=random.randint(1000, 9999))
    User.create(name='David', authorisation_code=random.randint(1000, 9999))