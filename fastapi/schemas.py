from pydantic import BaseModel

class AuthDetails(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str

