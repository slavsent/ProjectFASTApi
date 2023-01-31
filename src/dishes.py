from shemas import DishBaseSchema
from modeling import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from core.db import get_db
from setredis import client
#import aioredis
import pickle


def dish_list(menu_id: str, submenu_id: str, db: Session = Depends(get_db)) -> list:
    """
    Возвращает список блюд у определенного меню и определеного подменю или пустой лист []
    :param menu_id: определенное меню по id
    :param submenu_id: определенное подменю по id
    :param db: открытие сеанса к БД
    :return: [] или список блюд
    """
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    cache = client.get('dishes')
    if cache is not None:
        return pickle.loads(cache)

    dish = db.query(models.Menu, models.SubmenuInMenu, models.SubMenu, models.DishInSubmenu, models.Dish). \
        with_entities(models.Dish.title, models.Dish.description, models.Dish.price).filter(
        models.Menu.id == menu_id
    ).filter(
        models.SubmenuInMenu.menu == models.Menu.id
    ).filter(
#        models.SubMenu.id == models.SubmenuInMenu.id and models.SubMenu.id == submenu_id
        models.SubMenu.id == submenu_id and models.SubMenu.id == models.SubmenuInMenu.id
    ).filter(
        models.DishInSubmenu.submenus == models.SubMenu.id
    ).filter(
        models.Dish.id == models.DishInSubmenu.dishes
    ).all()
    if dish:
        client.setex('dishes', 3600, pickle.dumps(dish))
        return dish
    else:
        client.setex('dishes', 3600, pickle.dumps([]))
        return []


def dish_create(menu_id: str, submenu_id: str, payload: DishBaseSchema, db: Session = Depends(get_db)) -> object:
    """
    Создание блюда у определенного меню и определеного подменю
    :param menu_id: определенное меню по id
    :param submenu_id: определенное подменю по id
    :param payload: данные по блюду
    :param db: открытие сеанса к БД
    :return: объект с созданным блюдом
    """
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
        cache = client.get('dishes')
        if cache is not None:
            client.delete('dishes')
        client.delete('menus')
        client.delete('submenus')
        client.delete(menu_id)
        client.delete(submenu_id)
        return new_dish


def dish_update(menu_id: str, submenu_id: str, dish_id: str, payload: DishBaseSchema, db: Session = Depends(get_db)) -> object:
    """
    Обновление блюда у определенного меню и определеного подменю
    :param menu_id: определенное меню по id
    :param submenu_id: определенное подменю по id
    :param dish_id: определенное блюдо по id
    :param payload: новые данные блюда
    :param db: открытие сеанса к БД
    :return: объект с обновленным блюдом
    """
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    #    int(dish_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    if dish_id == 'null':
        client.delete('menus')
        client.delete('submenus')
        client.delete('dishes')
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

            cache = client.get(dish_id)
            if cache is not None:
                client.setex(dish_id, 3600, pickle.dumps(dish_query))
                client.delete('dishes')

            return dish_query


def dish_read(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)) -> object:
    """
    Получение информации по id блюда у определенного меню и определеного подменю
    :param menu_id: определенное меню по id
    :param submenu_id: определенное подменю по id
    :param dish_id: определенное блюдо по id
    :param db: открытие сеанса к БД
    :return: объект с выбранным по id блюдом
    """
    if dish_id == 'null':
        client.delete('menus')
        client.delete('submenus')
        client.delete('dishes')
        return {"detail": "dish not found"}
    else:
        # try:
        #    int(menu_id)
        #    int(submenu_id)
        #    int(dish_id)
        # except ValueError:
        #    return {"detail": "dish not found"}
        # else:
        cache = client.get(dish_id)
        if cache is not None:
            return pickle.loads(cache)

        dish = db.query(models.Dish).get(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")
        client.setex(dish_id, 3600, pickle.dumps(dish))

        return dish


def dish_delete(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)) -> object:
    """
    Уладение блюда у определенного меню и определеного подменю с корректиовкой данных в меню и подменю
    :param menu_id: определенное меню по id
    :param submenu_id: определенное подменю по id
    :param dish_id: определенное блюдо по id
    :param db: открытие сеанса к БД
    :return: объект с информацией, что блюдо удалено или сообщеением, что такого блюда нет
    """
    # try:
    #    int(menu_id)
    #    int(submenu_id)
    #    int(dish_id)
    # except ValueError:
    #    return {"detail": "dish not found"}
    # else:
    cache = client.get(dish_id)
    if cache is not None:
        client.delete(dish_id)
    client.delete('menus')
    client.delete('submenus')
    client.delete('dishes')
    client.delete(menu_id)
    client.delete(submenu_id)

    if dish_id == 'null':
        return {"detail": "dish not found"}
    else:
        dish_query = db.query(models.Dish).filter(models.Dish.id == dish_id)
        dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
        update_submenus = db.query(models.SubMenu).get(submenu_id)
        update_submenus.dishes_count -= 1
        update_menu = db.query(models.Menu).get(menu_id)
        update_menu.dishes_count -= 1
        dish_in_submenu = db.query(models.DishInSubmenu).filter(models.DishInSubmenu.dishes == dish_id)
        dish_in_submenu.delete(synchronize_session=False)
        dish_query.delete(synchronize_session=False)
        db.commit()
        return {"status": True, "message": "The dish has been deleted"}