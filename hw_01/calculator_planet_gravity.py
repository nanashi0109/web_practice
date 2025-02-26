G = 6.67 * 10 ** -11

planets = {
    "mercury": {"mass": 3.3011*10**23, "radius": 2439700},
    "venus": {"mass": 4.867*10**24, "radius": 6051800},
    "earth": {"mass": 5.9722*10**24, "radius": 6371000},
    "mars": {"mass": 6.4171*10**23, "radius": 3389500},
    "jupiter": {"mass": 1.8982*10**27, "radius": 69911000},
    "saturn": {"mass": 5.6834*10**26, "radius": 58232000},
    "uranus": {"mass": 8.681*10**25, "radius": 25362000},
    "neptune": {"mass": 1.9241*10**26, "radius": 24622000},
}


def calculate_planet_gravity(planet: str, height: int):
    planet = planet.lower()
    if planet not in planets.keys():
        raise ValueError

    planet_data = planets[planet]
    gravity = (planet_data["mass"]*G) / ((planet_data["radius"] + height)**2)

    return gravity
