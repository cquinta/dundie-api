"""User related data models"""
from typing import Optional
from sqlmodel import Field, SQLModel

class UserBase(SQLModel, table=True):
    """Represent the User model"""
    id: Optional[int] = Field(default=None, primary_key=True)   
    email: str = Field(unique=True,nullable=False)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    passsword: str = Field(nullable=False)
    name: str = Field(nullable=False)
    dept: str = Field(nullable=False)
    currency: str = Field(nullable=False)
    
    @property
    def superuser(self):
        """Users bellonging to the management department are admins"""
        return self.dept == "management"
    