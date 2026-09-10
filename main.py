from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Сервис меню столовой")

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class DishCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)


class Dish(DishCreate):
    id: int


dishes: list[Dish] = []
menu: dict[str, list[int]] = {}
next_dish_id = 1


def get_dish_or_404(dish_id: int) -> Dish:
    for dish in dishes:
        if dish.id == dish_id:
            return dish
    raise HTTPException(status_code=404, detail="Dish not found")


def validate_menu_date(menu_date: date) -> None:
    today = date.today()
    last_date = today + timedelta(days=30)
    if menu_date < today or menu_date > last_date:
        raise HTTPException(
            status_code=400,
            detail="Date must be within the next 31 days",
        )


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/dishes", response_model=list[Dish])
def get_dishes():
    return dishes


@app.get("/dishes/{dish_id}", response_model=Dish)
def get_dish(dish_id: int):
    return get_dish_or_404(dish_id)


@app.post("/dishes", response_model=Dish, status_code=201)
def create_dish(data: DishCreate):
    global next_dish_id
    dish = Dish(id=next_dish_id, **data.model_dump())
    dishes.append(dish)
    next_dish_id += 1
    return dish


@app.put("/dishes/{dish_id}", response_model=Dish)
def update_dish(dish_id: int, data: DishCreate):
    dish = get_dish_or_404(dish_id)
    dish.name = data.name
    dish.category = data.category
    return dish


@app.delete("/dishes/{dish_id}", status_code=204)
def delete_dish(dish_id: int):
    get_dish_or_404(dish_id)
    dishes[:] = [dish for dish in dishes if dish.id != dish_id]
    for dish_ids in menu.values():
        while dish_id in dish_ids:
            dish_ids.remove(dish_id)


@app.get("/menu")
def get_menu():
    result = []
    today = date.today()
    for offset in range(31):
        current_date = today + timedelta(days=offset)
        key = current_date.isoformat()
        result.append(
            {
                "date": key,
                "dishes": [get_dish_or_404(dish_id) for dish_id in menu.get(key, [])],
            }
        )
    return result


@app.get("/menu/{menu_date}")
def get_day_menu(menu_date: date):
    validate_menu_date(menu_date)
    key = menu_date.isoformat()
    return {
        "date": key,
        "dishes": [get_dish_or_404(dish_id) for dish_id in menu.get(key, [])],
    }


@app.post("/menu/{menu_date}/dishes/{dish_id}", status_code=201)
def add_dish_to_menu(menu_date: date, dish_id: int):
    validate_menu_date(menu_date)
    get_dish_or_404(dish_id)
    key = menu_date.isoformat()
    day_menu = menu.setdefault(key, [])
    if dish_id in day_menu:
        raise HTTPException(status_code=400, detail="Dish already added to this date")
    day_menu.append(dish_id)
    return {"message": "Dish added to menu"}


@app.delete("/menu/{menu_date}/dishes/{dish_id}", status_code=204)
def delete_dish_from_menu(menu_date: date, dish_id: int):
    validate_menu_date(menu_date)
    key = menu_date.isoformat()
    day_menu = menu.get(key, [])
    if dish_id not in day_menu:
        raise HTTPException(status_code=404, detail="Dish not found in menu for this date")
    day_menu.remove(dish_id)
