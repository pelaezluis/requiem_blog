from sqlmodel import Session,select
from app.models.view_model import View
from datetime import datetime
from typing_extensions import List, Optional
from app.schemas.view_schema import viewBasic,viewCreate,viewUpdate,viewDelete
from app.models.post_model import Post

def get_view_by_id(db:Session,view_id:int):
    statement = select(View).where(View.id == view_id)
    view = db.exec(statement).first()
    return view

def get_view_all(db:Session)->List[View]:
    statement = select(View)
    views = db.exec(statement).all()
    return views


def create_view(db: Session, view: viewCreate, post_id:int):
    db_view = View(
        view_count=view.view_count,
        post_id=post_id,
        last_view=datetime.utcnow()
    )
    db.add(db_view)
    db.commit()
    db.refresh(db_view)
    return db_view

def update_view(db: Session, view_id: int, view_update: viewUpdate):
    db_view = db.get(View, view_id)
    if not db_view:
        return None
    db_view.last_view = datetime.utcnow() if view_update.last_view is None else view_update.last_view
    
    db.commit()
    db.refresh(db_view)
    return db_view

def get_views_by_post_id(db: Session, post_id: int) -> List[View]:
    statement = select(View).where(View.post_id == post_id)
    views = db.exec(statement).all()
    return views


def delete_view(db: Session, view_id: int) -> bool:
    statement = select(View).where(View.id == view_id)
    db_view = db.exec(statement).first()
    if db_view:
        db.delete(db_view)
        db.commit()
        return True
    return False


