def calculate_speed_fine(speed: int, limit: int):
    delta = speed - limit

    if delta <= 10:
        return 0
    elif delta <= 20:
        return 500
    elif delta <= 40:
        return 1500
    else:
        return 50 * delta
