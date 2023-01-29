from shemas import SubMenuBaseSchema
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter
from core.db import get_db
from src.submenus import submenu_list, submenu_create, submenu_read, submenu_update, submenu_delete

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus')


@router.get('/', status_code=status.HTTP_200_OK)
def get_submenu(menu_id: str, db: Session = Depends(get_db)):
    return submenu_list(menu_id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: str, payload: SubMenuBaseSchema, db: Session = Depends(get_db)):
    return submenu_create(menu_id, payload, db)


@router.patch('/{submenu_id}', status_code=status.HTTP_200_OK)
def update_submenu(menu_id: str, submenu_id: str, payload: SubMenuBaseSchema, db: Session = Depends(get_db)):
    return submenu_update(menu_id, submenu_id, payload, db)


@router.get('/{submenu_id}', status_code=status.HTTP_200_OK)
def get_read(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return submenu_read(menu_id, submenu_id, db)


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
def delete_post(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return submenu_delete(menu_id, submenu_id, db)
