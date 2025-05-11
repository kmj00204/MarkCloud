import uvicorn
import json
from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def load_data():
    with open("datas/trademark_sample.json", "r", encoding="utf-8") as f:
        return json.load(f)


def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d").strftime("%Y년 %m월 %d일")
    except Exception:
        return date_str


def process_data(data):
    date_keys = {
        "applicationDate",
        "publicationDate",
        "registrationDate",
        "internationalRegDate",
        "priorityClaimDateList"
    }
    for item in data:
        for key, value in item.items():
            if isinstance(value, list):
                if all(v is None for v in value):
                    item[key] = None
                else:
                    if key in date_keys:
                        value = [format_date(v)
                                 for v in value if v is not None]
                        item[key] = ',\n'.join(value)
                    else:
                        item[key] = ', '.join(value)

            if isinstance(value, str) and key in date_keys:
                item[key] = format_date(value)

            if item[key] is None:
                item[key] = '-'
    return data


@app.get("/", response_class=HTMLResponse)
def show_board(request: Request):
    data = process_data(load_data())
    return templates.TemplateResponse("board.html", {"request": request, "items": data})


@app.get("/search", response_class=HTMLResponse)
def search(request: Request,
           query: List[str] = Query(),
           field: List[str] = Query()
           ):

    data = process_data(load_data())

    for q, f in zip(query, field):
        data = [item for item in data if q.lower() in
                item.get(f, "").lower()]

    return templates.TemplateResponse("board.html", {"request": request, "items": data})


@app.get("/add", response_class=HTMLResponse)
def add(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
