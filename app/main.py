from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from typing import Dict
from typing import List
from pydantic import BaseModel
from pydantic import Field
import time
import logging
import json
import requests
import os
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta
from src.authentification import *
from src.weather_logic import *

app = FastAPI()

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)


app = FastAPI()
if os.getenv("DEPLOYMENT_TYPE") != "container":
    from dotenv import load_dotenv
    load_dotenv()

api_key = os.getenv("API_KEY")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def get_redirected():
    return RedirectResponse(url='/docs')
    # return{"message": "hi"}


@app.get("/api/V1/recommend/")
async def get_recommendation(params: CustomQueryParams = Depends(), current_user: User = Depends(get_current_active_user)):
    exclude_list = ["minutely", "alerts", "daily"]
    response = dict()
    logging.info(
        f"received weather request for lat: {params.lat}, lon:{params.lon}")
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={params.lat}&lon={params.lon}&exclude={exclude_list}&appid={api_key}&units=metric")
        response = r.json()
    except requests.exceptions.ConnectionError as e:
        logging.exception("Could not reach open weather api")
        raise HTTPException(
            status_code=408, detail="Open Weather api is currently not available")
        return 0
    if "cod" in response and response["cod"] == 401:
        logging.exception("Wrong API key for Openweather api")
        raise HTTPException(
            status_code=401, detail=response)
        return 0
    logging.info("sucessfully send request to api")

    clothing = clothing_descision(response["hourly"][0]["temp"])
    umbrella = umbrella_descision(response["hourly"][0]["pop"])
    uv_risk = uv_risk_descision(response["hourly"][0]["uvi"])

    return [{"clothing": clothing, "risk": uv_risk, "umbrella": umbrella}]
