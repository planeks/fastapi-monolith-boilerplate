from uuid import UUID
from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str
    


class UserCreateSchema(UserBaseSchema):
    password: str
    


class UserSchema(UserBaseSchema):
    id: UUID
    is_active: bool
    
    class Config:
        orm_mode = True
