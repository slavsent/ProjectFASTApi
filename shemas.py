from typing import List
from pydantic import BaseModel


class DishBaseSchema(BaseModel):
    id: str | None = None
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListDishResponse(BaseModel):
    status: str
    results: int
    notes: List[DishBaseSchema]


class SubMenuBaseSchema(BaseModel):
    id: str | None = None
    title: str
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListSubMenuResponse(BaseModel):
    status: str
    results: int
    notes: List[SubMenuBaseSchema]


class MenuBaseSchema(BaseModel):
    id: str | None = None
    title: str
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListMenuResponse(BaseModel):
    status: str
    results: int
    notes: List[MenuBaseSchema]
