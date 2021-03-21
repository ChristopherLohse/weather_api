FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV DEPLOYMENT_TYPE container
# Copy files
COPY ./app /app

RUN pip install -r requirements.txt
