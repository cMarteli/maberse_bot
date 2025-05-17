# weather.py

# import the module
import python_weather

LOCATION = "Perth"


async def getweather() -> None:
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from a city
        weather = await client.get(LOCATION)

        # returns the current day's forecast temperature (int)
        return (weather.temperature)


def getLocation():
    return LOCATION
