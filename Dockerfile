FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV DEPLOYMENT_TYPE container
# Update packages
# RUN apt-get update -y
# RUN apt-get upgrade -y

# Set dir for error logs
#ENV ERROR_LOG='/app/logging.log'


# Copy files
COPY ./app /app

RUN pip install -r requirements.txt
