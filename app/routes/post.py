from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database.database import engine
from app.schemas.user_schema import UserRead
from app.seguridad.seguridad_login import get_current_user
import app.crud.post_crud as crud
from app.schemas.post_schema import PostCreate,PostRead,PostUpdate
from typing_extensions import List, Optional,Union
router = APIRouter()

def get_db():
    db = Session(engine)
    try: 
        yield db
    finally:
        db.close()

#crear post
@router.post("/post", response_model=PostRead)
def create_post(post:PostCreate,db:Session= Depends(get_db),current_user:UserRead=Depends(get_current_user)):
    return crud.create_post(db,post,user_id=current_user.id)

#ruta para obtener todos los post
@router.get("/posts/all", response_model=List[PostRead])
def posts_all (db:Session=Depends(get_db), current_user:UserRead=Depends(get_current_user)):
    posts = crud.get_posts_all(db)
    return posts

#obtener post por id
@router.get('/post/{id}', response_model=PostRead)
def get_post(post_id:int,current_user: UserRead = Depends(get_current_user), db:Session= Depends(get_db)):
    post = crud.get_posts_by_id(db,post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post

#obtener una lista de post por user_id
@router.get("/posts/admin", response_model=List[PostRead])
def get_posts_for_user_id(user_id:int,db:Session=Depends(get_db),current_user: UserRead = Depends(get_current_user)):
    posts = crud.get_posts_user_id(db, user_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="post not found")
    return posts


#obtener lista por titulo
@router.get('/post/me/title', response_model=List[PostCreate])
def get_post_for_title(post_title:str,current_user: UserRead = Depends(get_current_user), db:Session= Depends(get_db)):
    post = crud.get_post_title(db,post_title)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post

#obtener post del usuario logueado
@router.get("/posts", response_model=List[PostUpdate])
def get_post_for_me(db:Session=Depends(get_db),current_user: UserRead = Depends(get_current_user)):
    posts = crud.get_post_me(db,current_user.id)
    if posts is None:
        raise HTTPException(status_code=404, detail="post not found")
    return posts

#actualizar
@router.put('/update_post/{id}',response_model=Union[PostUpdate, dict])
def update_post(post_id: int, post_update: PostUpdate,current_user: UserRead = Depends(get_current_user), db:Session=Depends(get_db)):
    updated_post = crud.update_posts(db, post_id, post_update)
    if updated_post is None:
        return {"message": "Post not found"}
    return updated_post

@router.delete('/delete_post/{id}')
def delete_post(post_id: int, current_user: UserRead = Depends(get_current_user), db:Session=Depends(get_db)):
    deleted= crud.delete_post(db,post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}