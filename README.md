# Weather-api

Eine gehostete Version (IBM-Cloud) kann [hier](http://weather-api.christopherlohse.de:30000/ "Title") werden.
Um die API zu nutzen, muss zunächst durch einen Postrequest mit Username und Passwort ein 30 Minuten gültiges Bearertoken angefragt werden:

```
curl -X 'POST' \
  'http://weather-api.christopherlohse.de:30000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=admin&password=This_is_a_secure_password&scope=&client_id=&client_secret='
```
Mit dem zurückgebenden Accesstoken kann dann ein Getrequest an die API mit dem Bearer im Header gestellt werden:

```
curl -X 'GET' \
  'http://weather-api.christopherlohse.de:30000/api/V1/recommend/?lat=48.7823200&lon=9.1770200' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYxNjMyNTcxMH0.FgiF6Bx0FkTxO6icQsfPREwdY8rMheDML6VLt_82Gjs'
```

Der hier eingegebene Bearer muss mit dem zuvor generiertem Bearer ersetzt werden.
Die Openapi UI befindet sich unter dem bereits oben genanntem [Link](http://weather-api.christopherlohse.de:30000/ "Title").
Eine Openapi-JSON kann unter http://weather-api.christopherlohse.de:30000/openapi.json gefunden werden. Mit dieser JSON ist es z.B. möglich die API in einer anderen Programmiersprache nachzubauen oder direkt in z.B. [Postmann](https://learning.postman.com/docs/integrations/available-integrations/working-with-openAPI/) reinzuladen.
## Deployment mit Docker

Um die App lokal mit Docker zu starten sind im Vorhinein einige Schritte notwendig:
### 1. Environment-Variablen richtig setzen
Auf der höchsten Verzeichnisebene ist eine `.env_example` angelegt. Diese muss zunächst in `.env` umbenannt werden.
Die Datei sieht wie folgt aus:

```
API_KEY=your api key here
OPEN_WEATHER_URL=https://api.openweathermap.org/data/2.5/onecall
HASHED_PASSWORD=hashed password
SECRET_KEY=15c7bed506ea45c1073e0b3a3212d08e30d62a157c0f1399483ba4bfdd04c66e
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Für `API_KEY` muss der persönliche API-Key für die Openweather -API eingegeben werden.
Die url kann bei Bedarf durch Änderung von `OPEN_WEATHER_URL` angepasst werden.
Da die API über ein Passwort gesichert ist, muss zunächst ein Passwort-Hash zur Authentifizierung des User generiert werden. Dies lässt sich am einfachsten mit folgendem Befehl im Terminal erreichen: <br>
```
htpasswd -bnBC 10 "" password | tr -d ':\n'
```
Wobei das Wort `passwort` durch das gewünschte Passwort ersetzt werden muss. Der Konsolenoutput muss dann als Wert für `HASHED_PASSWORD`gesetzt werden.
Auch ein Secret Key für die Verschlüsselung des Bearer Tokens ist dafür notwendig. Für diesen wert in die Konsole
```
openssl rand -hex 32
```
eingeben und den Output als Wert für `SECRET_KEY` setzen.
### 3. Docker Image builden
```
docker build -t weather-api:latest .
```
eingeben
### 4. Docker Container starten
```
docker run --env-file ./.env --name weather-api-container -p80:80 weather-api:latest
````
Läd die eben erstellte .env file in den Container und lässt diesen laufen.
Auf Localhost 80 sollte nun die Swagger-UI für die API erscheinen.

## Deployment mit Kubernetes
Für ein Kubernetes-Deployment muss zunächst das Image entweder Lokal auf für z.B. Minikube zur Verfügung gestellt werden, oder auf eine Image Registry wie z.B. Docker Hub oder die IBM-Cloude Registry hochgeladen werden. Die Konfigurationsdateien für Kubernetes sind alle in dem `deployment` Ordner zu finden.
### 1. Secrets definieren
 Es werden für das Cluster entsprechend die Enviroment Variabeln gesetzt. Zunächst müssen in der secret.yaml, die im `deploymen` Ordner liegt, die Werte für `API_KEY`, `HASED_PASSWORD`, `SECRET_KEY` analog zu den in der .env definierten Variablen gesetzt werden.
```
kubectl apply -f deployment/secret.yaml
```
Definiert das Secret bei richtig gesetztem kubectl Kontext entsprechend.
## 2. Configmap definieren
In der Datei `config.yaml` können bei bedarf die url zur Konsumierten api angepasst werden und der Timeout in Minuten für das Bearer Token definiert werden.
Mit den eingesetzten Werten, funktioniert die Konfiguration allerdings auch.
```
kubectl apply -f deployment/config.yaml
```
eingebenn, um diese Werte zu definieren.

## 3. Deployment erstellen
In der deployment.yaml ggf. den Image Namen anpassen und dann mit

```
kubectl apply -f deployment/deployment.yaml
```
Das Deployment für das Image erzeugen.

## 4. Service für das deployment definieren

```
kubectl apply -f deployment/service.yaml
```

Definiert einen service für das weather-api-image deployement und exposed diesen Service öffentlich auf dem Port `30000`.


