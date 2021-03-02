# cera

API server for cera build using Django v3

## Running the server

### 1. Create a new postgres database. Run below in terminal:

```
> psql
psql (12.1)
Type "help" for help.

nayan=# CREATE DATABASE cera;
nayan=# CREATE USER python WITH PASSWORD 'password';
nayan=# GRANT ALL ON DATABASE cera TO python;
```

### 2. Create a new virtual environment. Run below in terminal:

```
python3 -m venv env
```

### 3. Activate the env

```
source env/bin/activate
```

### 4. Clone this repo and cd to cera.

### 5. Install the required python modules in the env. 

```
pip install -r requirements.txt
```

### 6. Put the shared .env file in cera/cera/ dir.

### 7. Run migration

```
python3 manage.py migrate
```

### 8. Create superuser for admin panel. The below command would prompt you for username, email and password. Please remember them for future use.

```
python3 manage.py createsuperuser
```

### 9. Run the server

```
python3 manage.py runserver
```

### 10. Visit http://127.0.0.1:8000/admin/ and provide the username and password created in step 8.

### 11. Register a new application
Go to DJANGO OAUTH TOOLKIT/Applications section of the web page and add a new application. Click on Add Application. Select client type as confidential. Authorization grant type as Resource owner password-based. Note down the auto generated client_id and client_secret and hit save.

### 12. Add a new user
Go to api/Users section and add a new user.

### 13. Using endpoints /o/token and /me
Hit http:127.0.0.1/o/token with client_id, client_secret, username, password, grant_type (as password) to get the access_token. 
Use the access_token in authorization header with Bearer to /me to get the user details.
```
