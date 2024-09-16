from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth.auth import create_access_token, get_password_hash, verify_password
from app.db_and_models.models import User, UserModel


async def create_user(user_model: UserModel, db: Session):
    stmt = select(User).where(User.email == user_model.email)
    existing_user: User = db.exec(stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="email exists!")
    user_model.password = get_password_hash(user_model.password)
    user_model = User.model_validate(user_model)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"success": f"user mit ID {user_model.id} erstellt"}


async def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
    existing_user = db.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Not able to be authenticated")
    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Not able to be authenticated")
    token = create_access_token(user=existing_user)
    return {"access_token": token, "token_type": "bearer"}
