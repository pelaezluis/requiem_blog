from sqlmodel import Session, select
from app.models.post_model import Post
from datetime import datetime
from typing_extensions import List, Optional
from app.schemas.post_schema import PostCreate, PostUpdate
"""
def check_existing_post(db:Session,post_id:int):
    existing_post= db.exec(select(Post).where(Post.id == post_id)).first
    if existing_post:
        return True
    return False"""

def get_posts_all(db:Session)-> List[Post]:
    statement = select(Post)
    posts = db.exec(statement).all()
    return posts



def create_post(db:Session,post:PostCreate, user_id:int):
    db_post = Post(
        title=post.title,
        description=post.description,
        post=post.post,
        image_url=post.image_url,
        song_url=post.song_url,
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_user_id(db:Session, user_id:int)->List[Post]:
    statement = select(Post).where(Post.user_id==user_id)
    posts = db.exec(statement).all()
    if not posts:
        return None
    return posts



def get_posts_by_id(db:Session, post_id:int)-> Optional[Post]:
    statement = select(Post).where(Post.id == post_id)
    post = db.exec(statement).first()
    if not post:
        return None
    return post


def get_post_me(db:Session, user_id:int):
    statement = select(Post).where(Post.user_id == user_id)
    posts = db.exec(statement).all()
    if not posts:
        return None
    return posts

def get_post_title(db:Session, title:str):
    statement = select(Post).where(Post.title == title)
    posts = db.exec(statement).all()
    if not posts:
        return None
    return posts


def update_posts(db:Session,post_id:int,post_update:PostUpdate)-> Optional[Post]:
    post = get_posts_by_id(db, post_id)
    if not post:
        return None
    
    # Verificar si hay cambios en alguna columna
    if post.dict(exclude={"update_at"}) == post_update.dict(exclude_unset=True):
        return {"message": "You have not modified anything"}
    
    # Actualizar solo las columnas que tienen cambios
    for field, value in post_update.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    # Actualizar la fecha y hora en el campo update_at
    post.update_at = datetime.utcnow()
    
    db.commit()
    db.refresh(post)
    return post
    

def delete_post(db:Session, post_id:int)-> bool:
    statement = select(Post).where(Post.id == post_id)
    db_post = db.exec(statement).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False




