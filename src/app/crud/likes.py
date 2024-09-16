from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Like, LikeModel, Post, User


async def create_like(
    like_model: LikeModel,
    db: Session,
    user_id: int,
):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    post = db.exec(select(Post).where(Post.id == like_model.post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    already_liked = db.exec(
        select(Like).where(Like.user_id == user_id, Like.post_id == like_model.post_id)
    ).first()
    if already_liked:
        raise HTTPException(status_code=400, detail="Already liked this post")
    like = Like(
        post_id=like_model.post_id,
        user_id=user_id,
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return {"success": f"Like added"}


async def delete_like(
    like_id: int,
    db: Session,
    user_id: int,
):
    like = db.exec(select(Like).where(Like.id == like_id)).first()
    if not like:
        raise HTTPException(status_code=404, detail="like not found")
    if like.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    db.delete(like)
    db.commit()
    return {"success": "like removed"}


async def get_like_of_post(post_id: int, db: Session):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    likes = db.exec(select(Like).where(Like.post_id == post_id)).all()
    return likes
