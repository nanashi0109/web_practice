from fastapi import FastAPI

from hw_01.password_generator import get_random_password
from hw_01.calculator_speed_fine import calculate_speed_fine
from hw_01.calculator_planet_gravity import calculate_planet_gravity

app = FastAPI()


@app.get("/password")
def password(length: str):
    if length.isdigit():
        return f"password: {get_random_password(int(length))}"
    return "Input integer"


@app.get("/gravity")
def gravity(planet: str, height: str):
    if not height.isdigit():
        return "Height should be integer"
    try:
        result_gravity = calculate_planet_gravity(planet, int(height))
    except ValueError:
        return "Planet not found"

    return f"gravity: {result_gravity}"


@app.get("/speed-fine")
def speeding_fine(speed: str, limit: str):
    if not (speed.isdigit() and limit.isdigit()):
        return "Input integer"

    fine = calculate_speed_fine(int(speed), int(limit))
    return f"fine: {fine} rubles"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
