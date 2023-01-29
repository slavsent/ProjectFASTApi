from sqlalchemy import Column, String, Integer, Text, ForeignKey, inspect
from sqlalchemy.orm import relationship
from uuid import uuid4
from core.db import Base
from sqlalchemy.dialects.postgresql import UUID


class Dish(Base):
    __tablename__ = "dish"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    description = Column(Text)
    price = Column(String)


class SubMenu(Base):
    __tablename__ = "submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    description = Column(Text)
    dishes_count = Column(Integer)


class Menu(Base):
    __tablename__ = "menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    description = Column(Text)
    submenus_count = Column(Integer)
    dishes_count = Column(Integer)


class SubmenuInMenu(Base):
    __tablename__ = "submenu_in_menu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    menu = Column(UUID(as_uuid=True), ForeignKey(Menu.id))
    submenu = Column(UUID(as_uuid=True), ForeignKey(SubMenu.id), unique=True)

    submenu_id = relationship(SubMenu, cascade="all, delete", backref="parent")
    menu_id = relationship(Menu, cascade="all, delete", backref="parent")


class DishInSubmenu(Base):
    __tablename__ = "dish_in_submenu"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    submenus = Column(UUID(as_uuid=True), ForeignKey(SubMenu.id))
    dishes = Column(UUID(as_uuid=True), ForeignKey(Dish.id), unique=True)

    submenus_id = relationship(
        SubMenu, cascade="all, delete", backref="parent_submenu",
    )
    dishes_id = relationship(Dish, cascade="all, delete", backref="parent")
