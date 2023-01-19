from shemas import DishBaseSchema
from modeling import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from core.db import get_db

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')


@router.get('/')
def get_dish(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    dish = db.query(models.Menu, models.SubmenuInMenu, models.SubMenu, models.DishInSubmenu, models.Dish). \
        with_entities(models.Dish.title, models.Dish.description, models.Dish.price).filter(
        models.Menu.id == menu_id
    ).filter(
        models.SubmenuInMenu.menu == models.Menu.id
    ).filter(
        models.SubMenu.id == submenu_id
    ).filter(
        models.DishInSubmenu.submenus == models.SubMenu.id
    ).filter(
        models.Dish.id == models.DishInSubmenu.dishes
    ).all()
    if dish:
        return dish
    else:
        return []


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: str, submenu_id: str, payload: DishBaseSchema, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    dish = db.query(models.Dish).filter(models.Dish.title == payload.title).first()
    if dish:
        return "This dish have"
    else:
        new_dish = models.Dish(title=payload.title, description=payload.description, price=payload.price)
        db.add(new_dish)
        db.commit()
        db.refresh(new_dish)
        update_menu = db.query(models.Menu).get(menu_id)
        update_menu.dishes_count += 1
        update_submenus = db.query(models.SubMenu).get(submenu_id)
        update_submenus.dishes_count += 1
        new_dish_in_submenu = models.DishInSubmenu(submenus=submenu_id, dishes=new_dish.id)
        db.add(new_dish_in_submenu)
        db.commit()
        db.refresh(new_dish)
        return new_dish


@router.patch('/{dish_id}')
def update_submenu(menu_id: str, submenu_id: str, dish_id: str, payload: DishBaseSchema, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    #    int(dish_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    if dish_id == 'null':
        return {"detail": "dish not found"}
    else:
        dish_query = db.query(models.Dish).get(dish_id)
        if not dish_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
        else:
            dish_query.title = payload.title
            dish_query.description = payload.description
            dish_query.price = payload.price
            db.commit()
            db.refresh(dish_query)
            return dish_query


@router.get('/{dish_id}')
def get_read(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    if dish_id == 'null':
        return {"detail": "dish not found"}
    else:
        # try:
        #    int(menu_id)
        #    int(submenu_id)
        #    int(dish_id)
        # except ValueError:
        #    return {"detail": "dish not found"}
        # else:
        dish = db.query(models.Dish).get(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
        return dish


@router.delete('/{dish_id}')
def delete_post(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    #    int(dish_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    if dish_id == 'null':
        return {"detail": "dish not found"}
    else:
        dish_query = db.query(models.Dish).filter(models.Dish.id == dish_id)
        if not dish_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
        update_submenus = db.query(models.SubMenu).get(submenu_id)
        update_submenus.dishes_count -= 1
        update_menu = db.query(models.Menu).get(menu_id)
        update_menu.dishes_count -= 1
        dish_in_submenu = db.query(models.DishInSubmenu).filter(models.DishInSubmenu.dishes == dish_id)
        dish_in_submenu.delete(synchronize_session=False)
        dish_query.delete(synchronize_session=False)
        db.commit()
        return {"status": True, "message": "The dish has been deleted"}
