from fastapi import FastAPI


app = FastAPI()

names_list = [
    {"id":1, "name":"ali"},
    {"id":2, "name":"maryam"},
    {"id":3, "name":"arousha"},
    {"id":4, "name":"aziz"},
    {"id":5, "name":"zahra"},
]

# /names (GET(RETRIEVE),POST(CREATE))
@app.get("/names")
def retrieve_names_list():
    return names_list


# /names/:id (GET(RETRIEVE),PUT/PATCH(UPDATE),DELETE)



@app.get("/")
def root():
    return {"message":"Hello World! "}

