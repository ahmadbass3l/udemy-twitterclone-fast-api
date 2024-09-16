from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Post, PostModel, User


async def create_post(post_model: PostModel, db: Session, user_id: int):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    post = Post(
        content=post_model.content,
        created_at=post_model.created_at,
        user_id=user_id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"success": f"Post mit ID {post.id} created by the user {user_id}"}


async def delete_post(post_id: int, db: Session, user_id: int):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db.delete(post)
    db.commit()
    return {"success": f"Deleted post with id: {post_id} by the user {user_id}"}


async def update_post(post_id: int, db: Session, user_id: int, post_model: PostModel):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    post.created_at = post_model.created_at
    post.content = post_model.content
    db.add(post)
    db.commit()
    # db.refresh(post)
    return {"success": f"Updated post with id: {post_id} by the user {user_id}"}


async def get_post(post_id: int, db: Session):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    return post


async def get_all_posts_by_user_id(user_id: int, db: Session):
    posts = db.exec(select(Post).where(Post.user_id == user_id)).all()
    return posts
