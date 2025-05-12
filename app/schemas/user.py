from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    photo: str
    fcm: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    photo: str