# 📱 financial-accounting

An app where you can manage your finances!

REST API for the app.

### 📝 Requirements

1. Python 3.10
2. PostgreSQL
3. Celery
4. Redis

### Setup

1. Clone the repository ```git clone https://github.com/artemkka12/financial-accounting.git```
2. Install poetry ```pip install poetry```
3. Install dependencies ```poetry install```
4. Install pre-commit hooks ```pre-commit install```

### 🔧 .env

```python
# DJANGO
SECRET_KEY=
DEBUG=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

SITE_URL=

# Redis
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

# Email
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

#### Run tests with coverage

```
coverage erase && coverage run manage.py test && coverage report
```

#### Run celery beat

```
celery -A config beat -l info
```

#### Run celery worker

```
celery -A config worker -l info
```

#### Deployment

``` python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
