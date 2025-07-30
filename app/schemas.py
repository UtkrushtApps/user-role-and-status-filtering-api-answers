from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    username: str
    role: str
    status: str

    class Config:
        orm_mode = True
