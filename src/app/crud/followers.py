from fastapi import HTTPException
from sqlmodel import Session, select

from app.crud.posts import delete_post
from app.db_and_models.models import Follower, FollowerModel, User


async def create_follower(
    follower_model: FollowerModel,
    db: Session,
    user_id: int,
):
    current_user = db.exec(select(User).where(User.id == user_id)).first()
    followed_user = db.exec(
        select(User).where(User.id == follower_model.follower_id)
    ).first()

    if not any((current_user, followed_user)):
        raise HTTPException(status_code=404, detail="Not Found!")

    already_followed = db.exec(
        select(Follower).where(
            Follower.user_id == user_id,
            Follower.follower_id == follower_model.follower_id,
        )
    ).first()
    if already_followed:
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} folgt {follower_model.follower_id} bereits",
        )
    follower = Follower(follower_id=follower_model.follower_id, user_id=user_id)
    db.add(follower)
    db.commit()
    db.refresh(follower)
    return {"Success": f"ID {user_id} folgt jetzt {follower_model.follower_id}"}


async def delete_following(follower_id: int, db: Session, user_id: int):
    follow = db.exec(
        select(Follower).where(Follower.user_id == user_id, Follower.id == follower_id)
    ).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Followership nicht gefunden")
    if follow.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    db.delete(follow)
    db.commit()
    return {"success": f"Followership beendet"}


async def get_following(
    user_id: int,
    db: Session,
):
    follower = db.exec(select(Follower).where(Follower.follower_id == user_id)).all()

    return follower
