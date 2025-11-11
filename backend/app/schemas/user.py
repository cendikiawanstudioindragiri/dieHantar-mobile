from pydantic import BaseModel, EmailStr
from app.schemas.token import Token  # re-export Token schema here for convenience


class UserBase(BaseModel):
	email: EmailStr
	full_name: str | None = None
	is_active: bool = True


class UserCreate(BaseModel):
	email: EmailStr
	password: str
	full_name: str | None = None


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


# Optional alias matching naming preference (Login vs LoginRequest)
class Login(LoginRequest):
	pass


class UserRead(UserBase):
	id: int

	class Config:
		from_attributes = True

