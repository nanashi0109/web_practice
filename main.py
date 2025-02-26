from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")


task_list = [
    {"header":"Hahaha", "description": "some description"}, 
    {"header":"Title 2", "description": "desc of second task"}
]


@app.get("/hi")
def greet():
    return {"message": "Hello!",
             "status": "ok"}


@app.post("/tasks")
def load(task: str = Body(emded=True)):
    return task_list.append(task)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
