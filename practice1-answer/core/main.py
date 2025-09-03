from fastapi import Body, FastAPI, File, UploadFile, Query, status, HTTPException, Path, Form
from fastapi.responses import JSONResponse
from typing import List
import random
from contextlib import asynccontextmanager
from schemas import CostCreateSchema, CostResponseSchema, CostUpdateSchema

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Application startup")
#     yield
#     print("Application shutdown")

app = FastAPI()

costs_db = [
    {
        "description": "descriptioneee",
        "id": 1,
        "amount": 10
    },
    {
        "description": "descriptionor",
        "id": 2,
        "amount": 20
    },
    {
        "description": "descr",
        "id": 3,
        "amount": 30
    },
    {
        "description": "descrip",
        "id": 4,
        "amount": 40
    },
    {
        "description": "description",
        "id": 5,
        "amount": 50
    },
    {
        "description": "script",
        "id": 6,
        "amount": 60
    }
]


@app.post("/cost", status_code = status.HTTP_201_CREATED, response_model=CostResponseSchema)
def create_cost(cost : CostCreateSchema):
    count_id = random.randint(6,100)
    cost_obj = {"id":count_id, "description": cost.description, "amount": cost.amount}
    costs_db.append(cost_obj)
    print(cost)
    return cost_obj

# READ
@app.get("/costs", status_code=status.HTTP_200_OK, response_model = List[CostResponseSchema])
def retrieve_costs():
    items = []
    for item in costs_db:
        items.append(item)
    return items

@app.get("/costs/", status_code=status.HTTP_200_OK, response_model = CostResponseSchema)
def retrieve_specific_costs(obj_id: str | None = Query(alias="search")):
    if obj_id:
        return [item for item in costs_db if str(item["id"]) == obj_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object Not Found")

# Update
@app.put("/costs/", status_code=status.HTTP_200_OK, response_model = CostResponseSchema)
def costs_update(cost: CostUpdateSchema, obj_id: str | None = Query(alias="search")):
    for item in costs_db:
        if str(item["id"]) == obj_id:
            item["amount"] = cost.amount
            item["description"] = cost.description
            return {"id": obj_id, "description": cost.description, "amount": cost.amount}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="object Not Found")

# DELETE
@app.delete("/costs/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def cost_delete(item_id: str):
    for item in enumerate(costs_db):
        if str(item["id"]) == item_id:
            costs_db.remove(item)
            return JSONResponse(content={"message" : f"Name with ID {item_id} deleted successfully"}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="object Not Found")

@app.get("/names")
def retrieve_names_list(q: str | None = Query(alias="search",description="This is a description",example="ali", default = None, max_length=50)):
    if q:
        return [item for item in names_db if item["name"] == q]
        # [operation iteration condition]
    return names_db

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {"filename": file.filename, "content-type": file.content_type, "file_size": len(content)}

@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile]):
    return [
        {"filename": file.filename, "content_type": file.content_type} 
        for file in files
    ]