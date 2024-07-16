from fastapi import FastAPI, Query, status, HTTPException,Path,Form
from fastapi.responses import JSONResponse
import random

app = FastAPI()

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "maryam"},
    {"id": 3, "name": "arousha"},
    {"id": 4, "name": "aziz"},
    {"id": 5, "name": "zahra"},
    {"id": 6, "name": "ali"},
    {"id": 7, "name": "ali"},
]

# /names (GET(RETRIEVE),POST(CREATE))


@app.get("/names")
def retrieve_names_list(q: str | None = Query(deprecated=True,
                                              alias="search",
                                              description="it will be searched with the title you provided",
                                              example="ali",
                                              default=None,
                                              max_length=50)):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name: str = Form()):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj


# /names/:id (GET(RETRIEVE),PUT/PATCH(UPDATE),DELETE)
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id: int = Path(alias="object_id",title="object id",description="the id of the name in names_list")):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="object not found")


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name_detail(name_id: int = Path(), name: str  = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="object not found")


@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(content={"detail": "object removed successfully"}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="object not found")


@app.get("/")
def root():
    content = {"message": "Hello World! "}
    return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)
