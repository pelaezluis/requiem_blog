from fastapi import APIRouter, HTTPException,Depends
from app.schemas.view_schema import viewCreate, viewBasic
from app.seguridad.seguridad_login import get_current_user
from typing_extensions import List
from app.schemas.user_schema import UserRead #para el esquema de seguridad

router = APIRouter()

views = {
    1:viewCreate(id=1,view_count=2,post_id=1)
}

#ruta crea view
@router.get("/views", response_model=List[viewCreate])
def get_views(current_user: UserRead = Depends(get_current_user)):
    return list(views.values())

@router.post("/views", response_model=viewCreate)
def create_view(view:viewBasic, current_user: UserRead = Depends(get_current_user)):
    view_id = max(views.keys()) + 1
    view_data = view.dict(exclude_unset=True)
    new_view = viewCreate(id=view_id,**view_data)
    views[view_id]=new_view
    return new_view

@router.delete("/views/{view_id}")
def delete_view(view_id:int,current_user: UserRead = Depends(get_current_user)):
    view = views.get(view_id)
    if view is None:
        raise HTTPException(status_code=404, detail="Views not found")
    del views[view_id]
    return view



