from shemas import MenuBaseSchema
from sqlalchemy.orm import Session
from core.db import get_db
from fastapi import Depends, status, APIRouter
from src.menus import menu_list, menu_create, menu_read, menu_update, menu_delete


router = APIRouter(prefix='/api/v1/menus')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_menu(db: Session = Depends(get_db)):
    return menu_list(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuBaseSchema, db: Session = Depends(get_db)):
    return menu_create(payload, db)


@router.patch('/{menu_id}', status_code=status.HTTP_200_OK)
def update_menu(menu_id: str, payload: MenuBaseSchema, db: Session = Depends(get_db)):
    return menu_update(menu_id, payload, db)


@router.get('/{menu_id}', status_code=status.HTTP_200_OK)
def get_read(menu_id: str, db: Session = Depends(get_db)):
    return menu_read(menu_id, db)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
def delete_post(menu_id: str, db: Session = Depends(get_db)):
    return menu_delete(menu_id, db)
