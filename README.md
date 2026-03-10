# Django Docker Setup

## Project Structure
```
project_root/
├── (Root Django Files)
├── manage.py
├── requirements.txt
│   ├── mikedinder/ (Your Django "mikedinder" App Files)
│   ├── app2/ (Your Django "app2" App Files)
│   ├── app3/ (Your Django "app3" App Files)
```

## Requirements
- Lorum Ipsum

## Services

- Must Manually Run `load_restaurants` command on First Build

## Access Points

- Django App: *http://localhost:8000* or *http://127.0.0.1:8000*
- Prod App: *https://django.mikedinder.com*
- PostgreSQL: *localhost:5432*
- Endpoint: *http://localhost:8000/api/v1/restaurants/search/?datetime=2026-02-14%2023:30*

## Common Commands

1. **Import Seed CSV File:**
   ```python
   python manage.py load_restaurants --path raw_data/restaurants.csv
   ```
   \* *Must Activate Virtual Environment First*

2. **Run Migrations Manually:**
   ```python
   python manage.py makemigrations
   python manage.py migrate
   ```
   \* *Must Activate Virtual Environment First*

3. **Create Superuser:**
   ```python
   python manage.py createsuperuser
   ```
   \* *Must Activate Virtual Environment First*

4. **Execute Django Tests:**
   ```python
   python manage.py test
   ```
   \* *Must Activate Virtual Environment First*

## Notes
- Lorum Ipsum
