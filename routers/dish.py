from shemas import DishBaseSchema
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter
from core.db import get_db
from src.dishes import dish_list, dish_create, dish_read, dish_update, dish_delete

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@router.get('/', status_code=status.HTTP_200_OK)
def get_dish(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return dish_list(menu_id, submenu_id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: str, submenu_id: str, payload: DishBaseSchema, db: Session = Depends(get_db)):
    return dish_create(menu_id, submenu_id, payload, db)


@router.patch('/{dish_id}', status_code=status.HTTP_200_OK)
def update_dish(menu_id: str, submenu_id: str, dish_id: str, payload: DishBaseSchema, db: Session = Depends(get_db)):
    return dish_update(menu_id, submenu_id, dish_id, payload, db)


@router.get('/{dish_id}', status_code=status.HTTP_200_OK)
def get_read(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return dish_read(menu_id, submenu_id, dish_id, db)


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
def delete_post(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return dish_delete(menu_id, submenu_id, dish_id, db)
