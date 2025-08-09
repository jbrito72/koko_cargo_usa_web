from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_username(*, session: Session, username: str) -> User | None:
    """Get user by ID or nombres (username)"""
    # Check if input is a numeric ID
    if username.isdigit():
        statement = select(User).where(User.id == int(username))
    else:
        # Search by nombres (username)
        statement = select(User).where(User.nombres == username)
    
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    """Authenticate user with ID/nombres and password (uses password_hash if exists)"""
    db_user = get_user_by_username(session=session, username=username)
    if not db_user:
        return None
    
    # Check if password_hash exists (user has logged in before)
    if db_user.password_hash:
        # Use bcrypt verification with the hashed password
        if not verify_password(password, db_user.password_hash):
            return None
    else:
        # No hash yet, compare with plain text password
        if password != db_user.password:
            return None
        # Generate and save hash for future logins (but keep original password intact)
        db_user.password_hash = get_password_hash(password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        print(f"Password hash generated for user {db_user.nombres} (original password unchanged)")
    
    return db_user