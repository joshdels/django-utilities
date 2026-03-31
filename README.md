# django-next-ts-water-utilities

This project is designed to manage water utilities engineering projects, transforming CAD files into georeferenced data and deploying them on a WebGIS platform.
 It aims to provide a scalable, maintainable system for utilities management.
---

## Methods
This project follows the AGILE methodology to allow iterative development and flexibility.

techstack

1. django rest-framework
  - jwt authentication
  - routers api endpoints
2. Docker 
3. Github Actions


---

### Gettings started
For testing please make it ensure you have a postgres installed with postgis enabled

Ensure your .env.local   file looks like this
```
PROJECT_KEY="django-project-key"
   
ALLOWED_HOSTS="host"
DEBUG=False

# database postgres
DB_NAME="db-name"
DB_USER="user-name"
DB_PASSWORD="your-password"
DB_HOST="db-connected-to"
DB_PORT="port"

CORS_URL="your-frontend-url"

```


```
python3 -m venv .venv
pip install -r requirements.txt
python migrate
python manage.py runserver
python manage.py migrate
```



