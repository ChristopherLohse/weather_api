# Weather-api
Aufgabe war es eine Wrapper-API für die Open-Weather-API zu bauen, die mit folgender Business-Logik funktioniert:
>Der Microservice „bewertet“ die nächste Stunde in der Vorhersage, d.h. Sie benutzen die Vorhersagedaten desArray-Elementshourly[1] für Temperatur (temp), UV-Index (uvi) und Niederschlagswahrscheinlichkeit (pop, probability of precipation).•Die Temperatur soll einen von drei Entscheidungswerten erzeugen: "tshirt" (> 12 °C), "sweater" (≤ 12 °C und > 5 °C)oder "coat" (≤ 5 °C).  Variablenname: clothes•Der UV-Index-Wert liefert eine Risikobewertung ("low" – "extreme", Einteilung siehe https://en.wikipedia.org/wiki/Ultraviolet_index). Implementieren Sie „low“, „moderate“ und „high“. Variablenname: risk•Die Niederschlagswahrscheinlichkeit pop kann einen Wert zwischen 0 (kein Niederschlag) und 1 (100 % Wahrscheinlichkeit) annehmen. pop < 0.1 (10 %) ergibt den Wert "no", pop ≥ 0.1 den Wert "yes". Variablenname: umbrellaDas Ergebnis soll als Typ „application/json“ an das Frontend übergeben werden, z.B.:{"clothes": "tshirt", "risk": "moderate", "umbrella": "no"}

Die API wurde mit Python in dem Framework Fastapi umgesetzt und richtet sich in der Struktur an der Standard Fastapi/Python Projektstruktur mit einem Ordner `app` außerhalb, in dem eine Datei 'main.py' liegt. In der main.py werden die API-Routen definiert und die weitere Logik wie Authentifizierung und die Businneslogik ist in zwei weiteren Files in dem Unterordner `app/src` definiert. Die Businesslogik ist in `app/src/weather_logic.py` definiert und die Authentifizierung in `app/src/authentification.py`.

Wie in der `openapi.json` Datei zu sehen ist, wurden gängige Exceptions gehandelt. So wird eine Exception zurückgeben, wenn der Open-Weather-API-Key falsch ist oder die API zurzeit gerade nicht erreichbar ist. Außerdem wird eine validierung der Input Daten vorgenommen, bei der Überprüft wird, ob es sich bei den eingebenen Werten um Floatingpoint-Numbers in dem gültigen Bereich für Latitude (-90 bis 90) und Longitude(-180 bis 180) befinden. Dieses Exceptionhandling ist in der Datei 'app/main.py' definiert.

Eine gehostete Version kann [hier](http://weather-api.christopherlohse.de "Title") gefunden werden.
Um die API zu nutzen, muss zunächst durch einen Postrequest mit Username und Passwort ein 30 Minuten gültiges Bearertoken angefragt werden:
(hier ist der Nutzer `Harald-U`und das Passwort `kubernetes`)
```
curl -X 'POST' \
  'http://weather-api.christopherlohse.de:30000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=Harald-U&password=kubernetes&scope=&client_id=&client_secret='
```
Die hier angegebenen Nutzerdaten sind in der gehostesten API freigeschaltet, allerdings nicht bei der selbstgehosteten.
Mit dem zurückgebenden Accesstoken kann dann ein Getrequest an die API mit dem Bearer im Header gestellt werden:

```
curl -X 'GET' \
  'http://weather-api.christopherlohse.de:30000/api/V1/recommend/?lat=48.7823200&lon=9.1770200' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYxNjMyNTcxMH0.FgiF6Bx0FkTxO6icQsfPREwdY8rMheDML6VLt_82Gjs'
```

Der hier eingegebene Bearer muss mit dem zuvor generiertem Bearer ersetzt werden.
Die Openapi UI befindet sich unter dem bereits oben genanntem [Link](http://weather-api.christopherlohse.de/ "Title").
Eine Openapi-JSON kann unter http://weather-api.christopherlohse.de/openapi.json gefunden werden. Mit dieser JSON ist es z.B. möglich die API in einer anderen Programmiersprache nachzubauen oder direkt in z.B. [Postmann](https://learning.postman.com/docs/integrations/available-integrations/working-with-openAPI/) reinzuladen.

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
Da die API über ein Passwort gesichert ist, muss zunächst ein Passwort-Hash zur Authentifizierung des User generiert werden. Dies lässt sich am einfachsten mit folgendem Befehl im Terminal erreichen:
```
htpasswd -bnBC 10 "" password | tr -d ':\n'
```
Wobei das Wort `password` durch das gewünschte Passwort ersetzt werden muss. Der Konsolenoutput (ohne das % am Ende) muss dann als Wert für `HASHED_PASSWORD`gesetzt werden.
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
Auf localhost:80 sollte nun die Swagger-UI für die API erscheinen. Der Authentifizierungsprozess läuft so wie oben beschreiben ab, mit dem Unterschied, dass der Username `admin` ist und das Passwort das in 1. ausgewählte Passwort. Natürlich wäre hier eine datenbankanbindung die sinnvollere Lösung für das passwort, aber dies wäre zu aufwendig für den Scope des Projektes.

## Deployment mit Kubernetes
Für ein Kubernetes-Deployment muss zunächst das Image entweder Lokal auf für z.B. Minikube zur Verfügung gestellt werden, oder auf eine Image Registry wie z.B. Docker Hub oder die IBM-Cloude Registry hochgeladen werden. Die Konfigurationsdateien für Kubernetes sind alle in dem `deployment` Ordner zu finden.
### 1. Secrets definieren
 Es werden für das Cluster entsprechend die Enviroment Variabeln gesetzt. Zunächst müssen in der secret.yaml, die im `deployment` Ordner liegt, die Werte für `API_KEY`, `HASED_PASSWORD`, `SECRET_KEY` analog zu den in der .env definierten Variablen gesetzt werden.
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
Das Deployment für das Image erzeugen. In der deployment.yaml Datei wird das weather-api image in einem Pod mit einer Replica deployed und der Port 80 des Pods wird exposed. unter dem `env` Teil werden das definierte Secret und die definierte ConfigMap in die Enviroment Varibalen desPods geladen.

## 4. Service für das deployment definieren

```
kubectl apply -f deployment/service.yaml
```

Definiert einen Service für das weather-api-image deployement. Der Service leitet den im Deployment spezifizierten Port 80 weiter und exposed diesen Service öffentlich auf dem Port `30000` über einen NodePort.
