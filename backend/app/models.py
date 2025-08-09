from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)



# Database model, mapped to existing 'usuarios' table
class User(SQLModel, table=True):
    __tablename__ = "usuarios"  # Map to existing table
    __table_args__ = {"extend_existing": True}  # Allow mapping to existing table
    
    # Original fields from usuarios table
    id: int = Field(primary_key=True)
    nombres: str = Field(unique=False)  # Username for login
    password: str  # Always keeps plain text (original password)
    password_hash: str | None = Field(default=None)  # Hashed password (nullable)
    administrador: bool = Field(default=False)
    pesca: bool = Field(default=False)
    maquinaria: bool = Field(default=False)
    super_usuario: bool = Field(default=False)
    
    
    # Compatibility properties for the template system
    @property
    def email(self) -> str:
        """Return nombres as email for compatibility"""
        return f"{self.nombres}@local.com" if "@" not in self.nombres else self.nombres
    
    @property
    def is_active(self) -> bool:
        """All users are considered active"""
        return True
    
    @property
    def is_superuser(self) -> bool:
        """Map super_usuario or administrador to is_superuser"""
        return self.super_usuario or self.administrador
    
    @property
    def full_name(self) -> str:
        """Return nombres as full_name"""
        return self.nombres
    
    @property
    def hashed_password(self) -> str:
        """Return hashed password if exists, otherwise plain password"""
        # Prefer password_hash if it exists and is not empty
        if self.password_hash:
            return self.password_hash
        # Fallback to plain password (for backward compatibility)
        return self.password


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int  # Changed from UUID to int to match usuarios table


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
