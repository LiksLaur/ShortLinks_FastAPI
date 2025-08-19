
# Fast API project for shortening links

### The project does not contain registration, so it cannot ensure data security, since it does not create keys for each user, which leads to the fact that a random user could change and delete data using some requests. Therefore, the project is used only locally on your device

I used fastApi and psycopg2. The whole project is made in a virtual environment and with the following main packages:

| package  | version  | 
|----------|----------|
| fastapi  | 0.116.1  | 
| psycopg2 | 2.9.10   | 
| requests | 2.32.4   | 

#### For connect to database you need to have file in the root of the project data.json it should contain the following data: 

{ "database": "", "user": "", "password": "", "host": "localhost", "port":  }

here you need to enter data from the database


#### For create apikey you need to have file in the root of the project apiKey.json it should contain the following data: 

{ "key": "" }

here you need to enter data for apikey
```
```




             
             
## API Reference

- #### Make link shorter

```http
  GET /link
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `link` | `string` | **Required**. Link |
| `whishes` | `string` | **Optional**. Short link endpoint  |

### Answer
```
{
  {
    "linksInfo": {
      "link": "string",
      "shortLink": "string"
    },
      "errorLogs": {
      "errNumber": 0,
      "errDescription": "string"
    }
  }
}
```

- #### Get link info 

```http
  GET /infolink
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `shortLink`      | `string` | **Required**. Short link endpoint
| `apiKey`      | `string` | **Required**. Api key from apiKey.json |


### Answer
```
{
  "id": "number"
  "link":"string"
  "shortlink":"string"
  "created_at":"string"
}
```

- #### Redirect

```http
  GET /{shortLink}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `shortLink`      | `string` | **Required**. Short link endpoint


### Answer
```
Redirect to original site
```

- #### Delete Link

```http
  GET /{shortLink}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `shortLink`      | `string` | **Required**. Short link endpoint
| `apiKey`      | `string` | **Required**. Api key from apiKey.json |


### Answer
```
{
  "status": ""
}
```

- #### Change Link

```http
  GET /{shortLink}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `shortLink`      | `string` | **Required**. Short link endpoint|
| `newShortLink`      | `string` | **Required**. New short link endpoint|
| `apiKey`      | `string` | **Required**. Api key from apiKey.json |


### Answer
```
{
  "status": ""
}
```

### example 
curl -X 'GET' \
  'http://127.0.0.1:8000/link?link=https%3A%2F%2Freadme.so%2Fru%2Feditor&whishes=readme' \
  -H 'accept: application/json'

%2 = /

%3 = :
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install fastapi[all] psycopg2 requests
```

Start the server

```bash
  uvicorn app.main:app --reload  
```

You can see all endpoints on http://127.0.0.1:8000/docs