# pydantic => used for validation, type enforcing during runtime.
import pydantic
from typing import Optional
import json

class User(pydantic.BaseModel):
    username: str
    password: str
    age: int
    score: int
    email: Optional[str]
    phone: Optional[str]

    # to validate data
    # we create a classmethod, and it is a pydantic validator focusing on the username
    # this indicates that whenever we set the username, this will get called
    # whatever we return from this function will become the username.
    @pydantic.validator('username')
    @classmethod
    def username_valid(cls,value):
        if len(value) > 5:
            return value
        raise Exception('username should be longer than 5 letters')



    # if age, or score is less than 0. show error.
    @pydantic.validator('age','score')
    @classmethod
    def nums_valid(cls,value):
        if value >= 0:
            return value
        raise ValueError('age must be positive')


    #if either phone no or email is needed
    @pydantic.root_validator(pre=True)
    def validate_phone_or_email(cls,values):
        print(values)
        if 'email' in values or 'phone' in values:
            return values
        raise ValueError('need either email or phone')

user1 = User(username='sayak',password='qwe',age=20,score=95,email='emailemail')
# this will throw an error, because username is not greater than 5 letters.

user2 = User(username='ranasen',password='asdf',age=-2,score=89,email='fuckkkk')
# this will throw  age must be positive (type=value_error)

user3 = User(username='zombies',password='owfieha',age=12,score=77)
# this will throw  a valueerror need either email or phone (type=value_error


# we read the json data, convert it into a list of python dicts, 
# and for each element of that array, we unpack that element and 
# create a class from it
json_user = [User(**u) for u in json.load(open("user.json"))]
# now json_user is an array of python dicts


print(json_user)