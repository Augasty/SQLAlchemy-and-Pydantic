# SQLAlchemy is an object relation mapper (ORM), that allows us to map python classes and objects to database tables and entries.
# We create, delete or change a python object, the respective action will be translated into a database action without us having to write sql queries.

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR

# String, Integer, CHAR => these are basically datapipes for the columns
# Column => the column itself
# FOreignKey => the foreign key relationship of the databases we are going to define
# create_engine => the engine that we can connect to (because sqlalchemy is compatable with a bunch of database types)

# => the base class we are going to extend/inherit from
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
# sessionmaker will essentially make a session and then we can start the session and do stuff in the database

Base = declarative_base()


class Person(Base):
    # this will be the table name inside the database (sqlite database, in this case)
    __tablename__ = "people"

    ssn = Column('ssn', Integer, primary_key=True)
    # we are creating a column in the sql, which is an integer, and is the primary key
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender},{self.age})"
    
class Thing(Base):
    __tablename__ = "things"
    tid = Column('tid',Integer,primary_key=True)
    description = Column('description',String)
    owner = Column(Integer,ForeignKey("people.ssn"))

    def __init__(self,tid,description,owner):
        self.tid = tid
        self.description = description
        self.owner = owner
    
    def __repr__(self):
        return f"{self.tid} {self.description} owned by {self.owner}"


# we can chose the database to be either
# 1. in memory database (in the ram) => it will be a new database everytime we run the script
# 2. file database
engine = create_engine("sqlite:///mydb.db", echo=True)


# this takes all the classes that extend from Base and creates them in the database
# it connects to the engine and creates all these tables
Base.metadata.create_all(bind=engine)


# creating a session
Session = sessionmaker(bind=engine)
session = Session()


p1 = Person(12312,"Mike","Smith","M",35)
p2 = Person(45674,"Rana","Sen","M",22)
p3 = Person(87609,"Biju","Mandal","F",23)

t1 = Thing(1,"Car",p1.ssn)
t2 = Thing(4,"Bike",p3.ssn)
t3 = Thing(3,"Mug",p1.ssn)

session.add(p1)
session.add(p2)
session.add(p3)
session.add(t1)
session.add(t2)
session.add(t3)
session.commit()


results = session.query(Person).all() #we will get python objects from the db
print(results)
filtered_result = session.query(Person).filter(Person.age > 22)
for r in filtered_result:
    print(r)

things = session.query(Thing).all()
print(things)
# if we run this code without deleting the .db file, we will get an error, as we will already have a database

# writing a query to find out the things owned by p1
query_result = session.query(Thing.description,Person.firstname).filter(Thing.owner == Person.ssn).filter(Person.firstname == 'Mike')
for q in query_result:
    print(q)