from pydantic import BaseModel


class AuthResponse(BaseModel):
    id: int
    name: str
    email: str
    photo: str
    token: str

class AuthRequest(BaseModel):
    token: str
    fcm: str