from shemas import SubMenuBaseSchema
from modeling import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.sql import func
from core.db import get_db

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus')


@router.get('/')
def get_submenu(menu_id: str, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    # except ValueError:
    #    return {"detail": "submenu not found"}
    # else:
    submenu = db.query(models.Menu, models.SubmenuInMenu, models.SubMenu). \
        with_entities(models.SubMenu.title, models.SubMenu.description, models.SubMenu.dishes_count).filter(
        models.Menu.id == menu_id
    ).filter(
        models.SubmenuInMenu.menu == models.Menu.id
    ).filter(
        models.SubMenu.id == models.SubmenuInMenu.submenu
    ).all()
    print(submenu)
    if submenu:
        return submenu
    else:
        return []


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: str, payload: SubMenuBaseSchema, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    # except ValueError:
    #    return {"detail": "submenu not found"}
    # else:
    submenu = db.query(models.SubMenu).filter(models.SubMenu.title == payload.title).first()
    if submenu:
        return {"detail": "This submenu have"}
    else:
        new_submenu = models.SubMenu(title=payload.title, description=payload.description, dishes_count=0)
        db.add(new_submenu)
        db.commit()
        db.refresh(new_submenu)
        update_menu = db.query(models.Menu).get(menu_id)
        update_menu.submenus_count += 1
        new_submenu_in_menu = models.SubmenuInMenu(menu=menu_id, submenu=new_submenu.id)
        db.add(new_submenu_in_menu)
        db.commit()
        db.refresh(new_submenu)
        return new_submenu


@router.patch('/{submenu_id}')
def update_submenu(menu_id: str, submenu_id: str, payload: SubMenuBaseSchema, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    # except ValueError:
    #    return {"detail": "submenu not found"}
    # else:
    if submenu_id == 'null':
        return {"detail": "submenu not found"}
    else:
        submenu_query = db.query(models.SubMenu).get(submenu_id)
        if not submenu_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="submenu not found")
        else:
            submenu_query.title = payload.title
            submenu_query.description = payload.description
            db.commit()
            db.refresh(submenu_query)
            return submenu_query


@router.get('/{submenu_id}')
def get_read(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    if submenu_id == 'null':
        return {"detail": "submenu not found"}
    else:
        # try:
        #    int(menu_id)
        #    int(submenu_id)
        # except ValueError:
        #    return {"detail": "submenu not found"}
        # else:
        submenu = db.query(models.SubMenu).get(submenu_id)
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="submenu not found")
        return submenu


@router.delete('/{submenu_id}')
def delete_post(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    # except ValueError:
    #    return {"detail": "submenu not found"}
    # else:
    submenu_query = db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id)
    if not submenu_query:
        return {"detail": "submenu not found"}
    update_menu = db.query(models.Menu).get(menu_id)
    update_menu.submenus_count -= 1
    submenu_in_menu = db.query(models.SubmenuInMenu).filter(models.SubmenuInMenu.submenu == submenu_id)
    submenu_in_menu.delete(synchronize_session=False)
    while True:
        dish_in_submenu_try = db.query(models.DishInSubmenu).filter(models.DishInSubmenu.submenus == submenu_id).all()
        print(len(dish_in_submenu_try))
        if len(dish_in_submenu_try) > 0:
            dish_in_submenu = db.query(models.DishInSubmenu).filter(models.DishInSubmenu.submenus == submenu_id).first()
            dish_in_submenu_del = db.query(models.DishInSubmenu).filter(models.DishInSubmenu.id == dish_in_submenu.id)
            dishes = db.query(models.Dish).filter(models.Dish.id == dish_in_submenu.dishes)
            update_menu.dishes_count -= 1
            dish_in_submenu_del.delete(synchronize_session=False)
            dishes.delete(synchronize_session=False)
            db.commit()
        else:
            break
    submenu_query.delete(synchronize_session=False)
    db.commit()
    return {"status": True, "message": "The submenu has been deleted"}
