from fastapi import FastAPI
from core.db import engine
from modeling import models
from routers import dish, submenu, menu


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(dish.router, tags=['Dish'])
app.include_router(submenu.router, tags=['Submenu'])
app.include_router(menu.router, tags=['Menu'])


@app.get("/api/restoran")
def root():
    return {"message": "Welcome our Restoran"}
