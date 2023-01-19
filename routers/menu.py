from shemas import MenuBaseSchema
from modeling import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from core.db import get_db

router = APIRouter()


@router.get('/')
def get_menu(db: Session = Depends(get_db)):
    # skip = (page - 1) * limit

    # menu = db.query(models.Menu).filter(
    #    models.Menu.title.contains(search)).limit(limit).offset(skip).all()
    # return {'status': 'success', 'results': len(menu), 'menu': menu}
    menu = db.query(models.Menu).all()
    if menu:
        return menu
    else:
        return []


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuBaseSchema, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.title == payload.title).first()
    if menu:
        return {"detail": "This menu have"}
    else:
        new_menu = models.Menu(title=payload.title, description=payload.description, dishes_count=0)
        new_menu.submenus_count = 0
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        return new_menu


@router.patch('/{menu_id}')
def update_menu(menu_id: str, payload: MenuBaseSchema, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    # except ValueError:
    #    return {"detail": "menu not found"}
    # else:

    if menu_id == 'null':
        return {"detail": "menu not found"}
    else:
        menu_query = db.query(models.Menu).get(menu_id)
        if not menu_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={"detail": "menu not found"})
        else:
            menu_query.title = payload.title
            menu_query.description = payload.description
            db.commit()
            db.refresh(menu_query)
            return menu_query


@router.get('/{menu_id}')
def get_read(menu_id: str, db: Session = Depends(get_db)):
    if menu_id == 'null':
        return {"detail": "menu not found"}
    else:
        # try:
        #    int(menu_id)
        # except ValueError:
        #    return {"detail": "menu not found"}
        # else:
        menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="menu not found")
        menu = db.query(models.Menu).get(menu_id)
        return menu


@router.delete('/{menu_id}')
def delete_post(menu_id: str, db: Session = Depends(get_db)):
    # try:
    #    int(menu_id)
    # except ValueError:
    #    return {"detail": "menu not found"}
    # else:
    menu_query = db.query(models.Menu).filter(models.Menu.id == menu_id)
    if not menu_query:
        return {"detail": "menu not found"}
    else:
        menu_query.delete(synchronize_session=False)
        db.commit()
        return {"status": True, "message": "The menu has been deleted"}
