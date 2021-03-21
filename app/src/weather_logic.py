from fastapi import Query
import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)


def get_clothing_decision(temperature: float) -> str:
    logging.info(f"The Temperature in the requested place is {temperature}")
    if temperature > 12.0:
        return "T-shirt"
    if temperature <= 12.0 and temperature > 5:
        return "sweater"
    else:
        return "coat"


def get_umbrella_decision(pop: float) -> bool:
    logging.info(f"The propability to rain in the requested place is {pop}")
    if pop < 0.1:
        return False
    else:
        return True


def get_uv_risk_decision(uv_index: int) -> str:
    logging.info(f"The UV-Index in the requested place is {uv_index}")
    if uv_index <= 2:
        return "low"
    if uv_index <= 3 and uv_index < 5:
        return "moderate"
    else:
        return "high"


def get_response_body(response: dict) -> dict:
    '''
    Gives a recomendation of what to wear based on response of open weather api
    Parameters
    ----------
    response: dict
        The response of the open weather api
    Returns
    -------
    A dict objet containing the recomendation
    '''
    clothing = get_clothing_decision(response["hourly"][0]["temp"])
    umbrella = get_umbrella_decision(response["hourly"][0]["pop"])
    uv_risk = get_uv_risk_decision(response["hourly"][0]["uvi"])

    return {"clothing": clothing,
            "risk": uv_risk,
            "umbrella": umbrella}
