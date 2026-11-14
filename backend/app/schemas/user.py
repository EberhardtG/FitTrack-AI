from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """ 
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    model_config = ConfigDict( json_schema_extra={
                "example": {
                    "name": "John Doe",
                    "email": "user@example.com",
                    "password": "securepassword"
                }
            })  

class UserRead(BaseModel):
    """
    Schema for reading user data.
    """
    id: int
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe",
                "is_active": True
            }
        })

class UserLogin(BaseModel):
    """ 
    Schema for user login.
    """
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict( json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "securepassword"
        }
    })

class UserUpdate(BaseModel):
    """
    Schema for updating user data.
    """
    name: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = Field(default=None)

    model_config = ConfigDict( json_schema_extra={
        "example": {
            "name": "newname",
            "email": "newemail@example.com",
            "password": "newsecurepassword",
            "is_active": True
        }
    })

