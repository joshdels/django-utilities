# django-next-ts-water-utilities

This will be the water utilities projects. This aligns engineering projects into usable and scalable systems
this will turn the CAD files, georeference it then deploy on
WebGIS

---

## Methods
This project follows the AGILE methodology to allow iterative development and flexibility.

techstack

1. django rest-framework
  - jwt authentication
  - routers api endpoints
2. nextjs
  - tailwind prettier
3. maplibre

---

### Gettings started

For testing please make it ensure you have a postgres installed with postgis enabled

```
cd backend
python3 -m venv .venv
pip install -r requirements.txt
python migrate
python manage.py runserver
```

```
cd frontend
npm install
npm run dev
```
