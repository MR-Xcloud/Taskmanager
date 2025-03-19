# Taskmanager
A RESTful API for task management built using Django and DRF with JWT Authentication and a custom user model.

### Features

- Custom user model with email, password, confirm password, name, and contact number
- User registration and login via JWT
- CRUD operations for tasks
- Assign tasks to users
- Filter tasks by status
- JWT-based authentication
- AWS Lambda simulation

### Setup

1. Install dependencies:

    pip install -r requirements.txt

2. Apply migrations:

    python3 manage.py makemigrations 
    python3 manage.py migrate

3. Create a superuser (optional):

    python3 manage.py createsuperuser

## if not wanted to make superuser, u can use,
@ username = admin
@ password = admin12


4. Run the server:

    python3 manage.py runserver

### Endpoints

- `POST /api/register/` (User Registration)
- `POST /api/jwt/login/` (Obtain Access and Refresh Tokens)
- `POST /api/jwt/refresh/` (Refresh Access Token)
- `GET /api/users/` (List Users)
- `GET/POST /api/tasks/` (Create or List Tasks)
- `GET /api/tasks/assigned_by=me` (get the list of task assigned by particular user)
- `GET /api/tasks/status=completed/pending` (get the list of task based on status)
- `GET/PATCH/DELETE /api/tasks/<id>/` (Retrieve, Update, or Delete Task)
- Filter tasks by assigned user with `?assigned_by=me`


### BONUS

    if some problem occurs, then you can use Docker-compose file, before using that just ensure that Docker_deamon is already installed on your system and is currently active, then in terminal of IDE where is code is present just run (Docker-compose up) it will do all the initial work for you and you can check the logs in docker deamon logs.
