# Weather-api

## Deployment with Docker

Um die App lokal mit Docker zu starten sind im vorhinein einige Schritte notwenig:
### 1. Enviroment-Variablen richtig setzen
Auf der höchsten Verzeichnisebene ist eine `.env_example` angelegt. Diese muss zunächst in `.env` umbennant werden.
Die Datei sieht wie folgt aus:

```
API_KEY=your api key here
OPEN_WEATHER_URL=https://api.openweathermap.org/data/2.5/onecall
HASHED_PASSWORD=hashed password
SECRET_KEY=15c7bed506ea45c1073e0b3a3212d08e30d62a157c0f1399483ba4bfdd04c66e
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Für `API_KEY` muss der persönliche api-Key für die Openweather api eingegeben werden. 
Die url kann bei Bedarf durch Änderung von `OPEN_WEATHER_URL` angepasst werden.
Da die API über ein Passwort gesichert ist, muss zunächst ein Passwort-Hash zur Authetifizierung des User generiert werden. Dies lässt sich am einfachsten mit folgenden Befehl im Terminal erreichen: <br>
```
htpasswd -bnBC 10 "" password | tr -d ':\n
``` 
wobei das Wortt `passwort` durch das gewümschte passworz ersetzt werden muss. Der Konsolenoutput muss dann als Wert für `HASHED_PASSWORD`gesetzt werden. 
Auch ein Secret Key für die Verschlüsselung des Bearer Tokens ist dafür notwendig. Für diesen wert in die Konsole `openssl rand -hex 32` eingeben und den Output als Wert für `SECRET_KEY` setzen. 
### 3. Docker Imgage builden
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
eine gehostete Version (IBM-Cloud) kann [hier](http://weather-api.christopherlohse.de:30000/ "Title") werden.
