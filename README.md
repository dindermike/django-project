# Django Docker Setup

## Project Structure
```
project_root/
├── Dockerfile
├── docker-compose.yml
├── init-postgres.sh
├── app/
│   ├── manage.py
│   ├── requirements.txt
│   └── (your Django project files)
```

## Requirements
- Docker Desktop for Windows or Mac
- Your Django Project Must Live in the `/app/` Folder
- `requirements.txt` File Must Live in the `/app/` Folder
- Copy the entire contents of the `/app/.env.example` file into a newly created `.env` file that you create in the same `/app/` folder before running your build command.

## Quick Start

1. **Build and Start Containers:**
   ```python
   docker-compose up --build
   ```

2. **Start Containers (After First Build):**
   ```python
   docker-compose up
   ```

3. **Stop Containers:**
   ```python
   docker-compose down
   ```

4. **Stop and Remove Volumes:**
   ```python
   docker-compose down -v
   ```

## Services

- **postgres**: PostgreSQL 16.11 database (port `5433` on host Windows/Mac)
- **migrations**: Runs makemigrations and migrate on Startup
- **web**: Django Development Server (port `8000` on host)
- **web**: Must Manually Run `load_restaurants` on Startup, Only After First Build

## Access Points

- Django App: *http://localhost:8000* or *http://127.0.0.1:8000*
- PostgreSQL: *localhost:5433*
- Endpoint: *http://localhost:8000/api/v1/restaurants/search/?datetime=2026-02-14%2023:30*

## pgAdmin Connection Settings

Connect pgAdmin on Windows to your Docker PostgreSQL:

1. Open pgAdmin
2. Register/Create New Server with These Settings:
   - **General Tab:**
     - Name: *Docker - Liine*

   - **Connection Tab:**
     - Host: *localhost*
     - Port: *5433*
     - Maintenance Database: *postgres*
     - Username: *postgres*
     - Password: *dinder*

   - **Parameters/SSL Tab:**
     - SSL Mode: *prefer*

**pgAdmin Setup Screenshots**
![General Tab](/readme_images/pgAdmin-1.jpg)
![Connection Tab](/readme_images/pgAdmin-2.jpg)
![Parameters Tab](/readme_images/pgAdmin-3.jpg)

## Common Commands

1. **Access Web Container Shell:**
   ```python
   docker exec -it web bash
   docker-compose exec web bash
   ```

2. **Access postgres Container:**
   ```python
   docker exec -it django_postgres psql -U postgres -d dinder
   docker-compose exec postgres psql -U postgres -d dinder
   ```

3. **Import Seed CSV File:**
   ```python
   python manage.py load_restaurants --path app/raw_data/restaurants.csv
   ```
   \* *Must Access Web Container Shell First*

4. **Run Migrations Manually:**
   ```python
   python manage.py makemigrations
   python manage.py migrate
   ```
   \* *Must Access Web Container Shell First*

5. **Create Superuser:**
   ```python
   python manage.py createsuperuser
   ```
   \* *Must Access Web Container Shell First*

6. **Execute Django Tests:**
   ```python
   python manage.py test
   ```
   \* *Must Access Web Container Shell First*

## Notes
- PostgreSQL Data Persists in a Docker Volume
- The migrations Container Runs Once on Startup and Exits
- Code Changes in `/app/` Folder are Reflected Immediately (Volume Mounted, possible second or two delay)
- PostgreSQL is Configured to Accept Remote Connections for pgAdmin
- Superuser is not created, fixture files do not exist. A real world project would include these for developers in a local environment use-case, but it is not needed for our GET Request and this exercise.
- CSV File Data needs to be manually loaded on first build. In a real world scenario I would try to figure out how to include it in the Dockerfile to run only once. I couldn't figure that out and deemed it not critical to this exercise.
- Even though I have the password scattered about this repo as an Environment Variable, I would make this a secret variable in a real world scenario and never include it in the readme and/or helper images as I did here. This project's security is not critical and for educational/demonstration purposes only.
- Copy the entire contents of the `/app/.env.example` file into a newly created `.env` file that you create in the same `/app/` folder before running your build command.
