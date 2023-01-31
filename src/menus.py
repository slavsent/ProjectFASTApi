import json

from shemas import MenuBaseSchema
from modeling import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from core.db import get_db
from setredis import client
# import aioredis
import pickle


def menu_list(db: Session = Depends(get_db)) -> list:
    """
    Список меню или пустой []
    :param db: открытие сеанса к БД
    :return: Список меню или пустой []
    """
    cache = client.get('menus')
    if cache is not None:
        return pickle.loads(cache)
    menu = db.query(models.Menu).all()
    if menu:
        client.setex('menus', 3600, pickle.dumps(menu))
        return menu
    else:
        client.setex('menus', 3600, pickle.dumps([]))
        return []


def menu_create(payload: MenuBaseSchema, db: Session = Depends(get_db)) -> object:
    """
    Создание меню
    :param payload: данные по меню
    :param db: открытие сеанса к БД
    :return: объект с созданным меню
    """
    menu = db.query(models.Menu).filter(models.Menu.title == payload.title).first()
    if menu:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    else:
        new_menu = models.Menu(title=payload.title, description=payload.description, dishes_count=0)
        new_menu.submenus_count = 0
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        cache = client.get('menus')
        if cache is not None:
            client.delete('menus')
        return new_menu


def menu_update(menu_id: str, payload: MenuBaseSchema, db: Session = Depends(get_db)) -> object:
    """
    Обновление меню
    :param menu_id: определенное меню по id
    :param payload: новые данные меню
    :param db: открытие сеанса к БД
    :return: объект с обновленным меню
    """
    # try:
    #    int(menu_id)
    # except ValueError:
    #    return {"detail": "menu not found"}
    # else:

    if menu_id == 'null':
        client.delete('menus')
        return {"detail": "menu not found"}
    else:
        menu_query = db.query(models.Menu).get(menu_id)
        if not menu_query:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"detail": "menu not found"})
        else:
            menu_query.title = payload.title
            menu_query.description = payload.description
            db.commit()
            db.refresh(menu_query)
            cache = client.get(menu_id)
            if cache is not None:
                client.setex(menu_id, 3600, pickle.dumps(menu_query))
                client.delete('menus')
            return menu_query


def menu_read(menu_id: str, db: Session = Depends(get_db)) -> object:
    """
    Получение информации определенного меню по id
    :param menu_id: определенное меню по id
    :param db: открытие сеанса к БД
    :return: объект с выбранным по id меню
    """
    if menu_id == 'null':
        client.delete('menus')
        return {"detail": "menu not found"}
    else:

        cache = client.get(menu_id)
        if cache is not None:
            return pickle.loads(cache)

        # try:
        #    int(menu_id)
        # except ValueError:
        #    return {"detail": "menu not found"}
        # else:
        menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
        menu = db.query(models.Menu).get(menu_id)

        client.setex(menu_id, 3600, pickle.dumps(menu))

        return menu


def menu_delete(menu_id: str, db: Session = Depends(get_db)) -> object:
    """
    Уладение определенного меню
    :param menu_id: определенное меню по id
    :param db: открытие сеанса к БД
    :return: объект с информацией, что меню удалено или сообщеением, что такого меню нет
    """
    if menu_id == 'null':
        client.delete('menus')
        return {"detail": "menu not found"}
    else:
        # try:
        #    int(menu_id)
        # except ValueError:
        #    return {"detail": "menu not found"}
        # else:
        cache = client.get(menu_id)
        if cache is not None:
            client.delete(menu_id)
        client.delete('menus')
        menu_query = db.query(models.Menu).filter(models.Menu.id == menu_id)
        menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        if not menu:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
        else:
            menu_query.delete(synchronize_session=False)
            db.commit()
            return {"status_code": True, "message": "The menu has been deleted"}
