# SMS api using Django Rest Framework
This project is a Django Rest api for SMS 



## Requirements
Python 3.0+

```bash
pip install -r requirements.txt
  
```
## Deployment

To run this on local machine 
change DATABASES in settings.py with local postgre server credentials

```bash
  DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': ‘<database_name>’,
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
```
then migrate the models to the database
```bash
python manage.py makemigrations
python manage.py migrate
```
To start the server 
```bash 
python manage.py runserver
```
In new terminal start a redis server with
```bash
redis-server
```
## API Reference

#### POST sms as a json with text:STOP to STOP receiving message from a perticular sender for 4 hours

```http
  POST /inbound/sms/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `sender` | `int` | **Required**. phone number of a valid user |
 `to` | `int` | **Required**.phone number of authenticated user |
  `text` | `string` | **Required**. Message|

#### POST sms as a json to send a message to anathor user. Daily api call limit =50

```http
  POST /outbound/sms/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `sender` | `int` | **Required**. phone number of an authenticated user |
 `to` | `int` | **Required**.phone number of a valid user |
  `text` | `string` | **Required**. Message|
