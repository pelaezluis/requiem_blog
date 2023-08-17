from fastapi import APIRouter, HTTPException,Depends
from app.schemas.view_schema import viewCreate, viewBasic
from app.seguridad.seguridad_login import get_current_user
from typing_extensions import List
from app.schemas.user_schema import UserRead #para el esquema de seguridad
from sqlmodel import Session
from app.database.database import engine
from app.schemas.view_schema import viewCreate, viewUpdate
import app.crud.view_crud as crud
import app.crud.post_crud  as crudpost

router = APIRouter()


def get_db():
    db = Session(engine)
    try: 
        yield db
    finally:
        db.close()


#ruta crea view
@router.post("/views", response_model=viewCreate)
def create_view(post_id: int, view: viewBasic, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    post = crudpost.get_posts_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to create a view for this post")
    db_view = crud.create_view(db, view, post_id)
    return db_view

#actualizar solo last_view
@router.put("/views/{view_id}/", response_model=viewBasic)
def update_view(view_id: int, view_update: viewUpdate, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    db_view = crud.get_view_by_id(db, view_id)
    if not db_view:
        raise HTTPException(status_code=404, detail="View not found")
    post = crudpost.get_posts_by_id(db, db_view.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this view")
    updated_view = crud.update_view(db, view_id, view_update)
    if not updated_view:
        raise HTTPException(status_code=400, detail="Failed to update view")
    return updated_view

#obtener las views de un post
@router.get("/posts/{post_id}/views/", response_model=List[viewBasic])
def get_post_views(post_id: int, db: Session = Depends(get_db)):
    post = crudpost.get_posts_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    views = crud.get_views_by_post_id(db, post_id)
    return views

#obtener vista por id
@router.get("/views/{view_id}", response_model=list[viewCreate])
def get_views_all( db: Session = Depends(get_db),current_user: UserRead = Depends(get_current_user)):
    views = crud.get_view_all(db)
    if not views:
        raise HTTPException(status_code=404, detail="No views")
    return views



#eliminar view
@router.delete("/views/delete/{view_id}/")
def delete_view(view_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    db_view = crud.get_view_by_id(db, view_id)
    if not db_view:
        raise HTTPException(status_code=404, detail="View not found")
    post = crudpost.get_posts_by_id(db, db_view.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this view")
    deleted = crud.delete_view(db, view_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete view")
    return {"message": "View deleted successfully"}



