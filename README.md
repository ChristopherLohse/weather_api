# Weather-api

## Deployment with Docker

Um die App lokal mit Docker zu starten sind im vorhinein einige Schritte notwenig:
### 1. Enviroment-Variablen richtig setzen
Auf der höchsten Verzeichnisebene ist eine `.env_example` angelegt. Diese muss zunächst in `.env` umbennant werden.
Die Datei sieht wie folgt aus: <br>
`API_KEY= "your api key here" # enter your openweather api-key here
OPEN_WEATHER_URL = https://api.openweathermap.org/data/2.5/onecall #replace with different api if needed
HASHED_PASSWORD = "hashed password" # enter your generated hashed password here
SECRET_KEY = "15c7bed506ea45c1073e0b3a3212d08e30d62a157c0f1399483ba4bfdd04c66e" # enter you secret key generated with openssl rand -hex 32 here
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # change the expire time of bearer token if needed`

Für `API_KEY` muss der persönliche api-Key für die Openweather api eingegeben werden. 
Die url kann bei Bedarf durch Änderung von `OPEN_WEATHER_URL` angepasst werden.
Da die API über ein Passwort gesichert ist, muss zunächst ein Passwort-Hash zur Authetifizierung des User generiert werden. Dies lässt sich am einfachsten mit folgenden Befehl im Terminal erreichen: <br>
`htpasswd -bnBC 10 "" password | tr -d ':\n` wobei das Wortt `passwort` durch das gewümschte passworz ersetzt werden muss. Der Konsolenoutput muss dann als Wert für `HASHED_PASSWORD`gesetzt werden. 
Auch ein Secret Key für die Verschlüsselung des Bearer Tokens ist dafür notwendig. Für diesen wert in die Konsole `openssl rand -hex 32` eingeben und den Output als Wert für `SECRET_KEY` setzen. 
### 3. Docker Imgage builden
`docker build -t weather-api:latest .` eingeben
### 4. Docker Container starten
`docker run --env-file ./.env --name weather-api-container -p80:80 weather-api:latest` <br>
Läd die eben erstellte .env file in den Container und lässt diesen laufen.
Auf Localhost 80 sollte nun die Swagger-UI für die API erscheinen.

2. Item
