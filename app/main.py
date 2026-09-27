from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/data")
async def get_data():
    return {"message": "Hello World"}


@app.post("/api/data")
async def post_data():
    return {"message": "Hello World"}

