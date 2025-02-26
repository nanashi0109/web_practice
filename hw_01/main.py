from fastapi import FastAPI

from hw_01.password_generator import get_random_password

app = FastAPI()


@app.get("/password")
def password(length):
    if length.isdigit:
        return f"password: {get_random_password(int(length))}"
    return "Input integer"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
