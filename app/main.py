from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
import logging
import requests
import os
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta
from src.authentification import (
    authenticate_user,
    create_access_token,
    Token,
    OAuth2PasswordRequestForm,
    get_current_active_user,
    User,
    fake_users_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    status,
)
from src.weather_logic import get_response_body

tags_metadata = tags_metadata = [
    {
        "name": "Token",
        "description": "Receive a Bearer token with a valid username and password",
    },
    {
        "name": "Recommendation",
        "description": "Get a recommendation for your clothing, sun protection and the need for an Umbrella by Latitude and Longitude Values",
    },
]
app = FastAPI(
    openapi_tags=tags_metadata,
    title="Weather-API",
    docs_url="/",
    description="An University Project by Christopher Lohse",
    version="1.0.0",
)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)

if os.getenv("DEPLOYMENT_TYPE") != "container":
    from dotenv import load_dotenv

    load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("OPEN_WEATHER_URL")


@app.post("/token", response_model=Token, tags=["Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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


@app.get("/api/V1/recommend/", tags=["Recommendation"])
async def get_recommendation(
    lat: float = Query(
        ...,
        title="Latitude",
        description="The Latitude of the requested Location",
        ge=-90,
        le=90,
    ),
    lon: float = Query(
        ...,
        title="Latitude",
        description="The Longitude of the requested Location",
        ge=-180,
        le=180,
    ),
    current_user: User = Depends(get_current_active_user),
):
    exclude_list = ["minutely", "alerts", "daily"]
    response = dict()
    logging.info(f"received weather request for lat: {lat}, lon:{lon}")
    try:
        r = requests.get(
            f"{url}?lat={lat}&lon={lon}&exclude={exclude_list}&appid={api_key}&units=metric",
            timeout=1,
        )
        response = r.json()
    except requests.exceptions.Timeout as e:
        logging.exception("The Connection to open Weather api timed out")
        raise HTTPException(
            status_code=408, detail="The Connection to open Weather api timed out"
        )
        return 0
    if r.status_code == 401:
        logging.exception("Wrong API key for Openweather api")
        raise HTTPException(status_code=401, detail=response)
        return 0
    logging.info("sucessfully send request to api")

    return get_response_body(response)
