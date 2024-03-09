"""User related data models"""
from typing import Optional
from sqlmodel import Field, SQLModel
from dundie.security import HashedPassword
from pydantic import BaseModel, root_validator
from fastapi import HTTPException, status
from dundie.security import get_password_hash

class User(SQLModel, table=True):
    """Represent the User model"""
    id: Optional[int] = Field(default=None, primary_key=True)   
    email: str = Field(unique=True,nullable=False)
    avatar: Optional[str] = None
    username: str = Field(unique=True, nullable=False)
    bio: Optional[str] = None
    password: HashedPassword
    name: str = Field(nullable=False)
    dept: str = Field(nullable=False)
    currency: str = Field(nullable=False)
    
    @property
    def superuser(self):
        """Users bellonging to the management department are admins"""
        return self.dept == "management"
    

    
def generate_username(name:str) -> str:
    """Generate a slug  from user.name"""
    return name.lower().replace(" ", "_")

class UserResponse(BaseModel):
    """Serializer for User Response"""
    name: str
    username: str
    dept: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    currency: str
    
class UserRequest(BaseModel):
    """ Serializer for when we get the user data from the client"""
    name: str
    email: str
    dept: str
    password: str
    currency: str = "USD"
    username: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None

    @root_validator(pre=True)
    def generate_username_if_not_set(cls, values):
        """Generates username if not set"""
        if values.get("username") is None:
            values["username"] = generate_username(values["name"])
        return values

class UserProfilePatchRequest(BaseModel):
    avatar: Optional[str] = None
    bio: Optional[str] = None
class UserPasswordPatchRequest(BaseModel):
    password: str
    password_confirm: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        """Checks if passwords match"""
        if values.get("password") != values.get("password_confirm"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        return values

    @property
    def hashed_password(self) -> str:
        """Returns hashed password"""
        return get_password_hash(self.password)

# TODO: library slugify
    