from fastapi import Query
import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)

"""
Logic functions of the API
"""


def get_clothing_decision(temperature: float) -> str:
    """
    Gives suggestion for clothing based on the weather
    Parameters:
    ----------
    temperature: float
        The Temperature in degrees celsius
    Returns
    -------
    A Suggestion of what to wear : str
        Possible suggestions are: coat, T-shirt, sweater
    """
    logging.info(f"The Temperature in the requested place is {temperature}")
    if temperature > 12.0:
        return "T-shirt"
    if temperature <= 12.0 and temperature > 5:
        return "sweater"
    else:
        return "coat"


def get_umbrella_decision(pop: float) -> bool:
    """
    Gives suggestion if an Umbrella is necessary for a given probability to rain
    Parameters:
    ----------
    pop: float
        Percentages of the likelihood to rain
    Returns
    -------
    A Suggestion wether to wear an umbrella or not : bool
    """
    logging.info(f"The propability to rain in the requested place is {pop}")
    if pop < 0.1:
        return "no"
    else:
        return "yes"


def get_uv_risk_decision(uv_index: int) -> str:
    """
    Gives a risk estimation for a given UV-Index
    Parameters:
    ----------
    uv_index: int
        Uv index
    Returns
    -------
    A risk estimation : str
        Possible risks are, low, high and moderate
    """
    logging.info(f"The UV-Index in the requested place is {uv_index}")
    if uv_index <= 2:
        return "low"
    if uv_index <= 3 and uv_index < 5:
        return "moderate"
    else:
        return "high"


def get_response_body(response: dict) -> dict:
    """
    Gives a recomendation of what to wear based on response of open weather api
    Parameters
    ----------
    response: dict
        The response of the open weather api
    Returns
    -------
    A dict objet containing the recomendation
    """
    clothing = get_clothing_decision(response["hourly"][0]["temp"])
    umbrella = get_umbrella_decision(response["hourly"][0]["pop"])
    uv_risk = get_uv_risk_decision(response["hourly"][0]["uvi"])

    return {"clothing": clothing, "risk": uv_risk, "umbrella": umbrella}
