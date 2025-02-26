from fastapi import FastAPI

from hw_01.password_generator import get_random_password
from hw_01.calculator_speed_fine import calculate_speed_fine

app = FastAPI()


@app.get("/password")
def password(length: str):
    if length.isdigit():
        return f"password: {get_random_password(int(length))}"
    return "Input integer"


@app.get("/speed-fine")
def speeding_fine(speed: str, limit: str):
    if not (speed.isdigit() and limit.isdigit()):
        return "Input integer"

    fine = calculate_speed_fine(int(speed), int(limit))
    return f"fine: {fine} rubles"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
