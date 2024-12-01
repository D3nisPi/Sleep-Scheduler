# Sleep-Scheduler

## Description
Sleep-Scheduler is a project for tracking sleep 
and setting sleep goals.

## Features
- User registration and authentication
- Setting sleep notes (sleep time, quality rating, comments)
- Setting sleep goals

## Technology stack
- FastAPI: Framework for building APIs
- SQLAlchemy: ORM for database interactions
- Postgres: RDBMS
- Pydantic: Data validation and settings management
- Bcrypt: Secure password hashing
- PyJWT: JWT generation and validation

## Installation and Setup

### Install dependencies
Ensure you have Poetry installed, 

```commandline
pip install poetry
```

then run:

```commandline
poetry install
```

### Configure environment variables
Create a `.env` file in the root directory with the following content 
(check `.env.template` for example):

```
#.env
app.run.host=<host>
app.run.port=<port>

app.db.host=<database host>
app.db.port=<database port>
app.db.user=<database user>
app.db.password=<password>
app.db.database=<database name>

app.engine.echo=<0 | 1>
app.engine.pool_size=<pool size>
app.engine.max_overflow=<max overflow>

app.jwt.secret_key=<secret key>
app.jwt.algorithm=<algorithm>
app.jwt.access_token_expiration_minutes=<access token lifetime>
app.jwt.refresh_token_expiration_days=<refresh token lifetime>
```

### Start the server
Launch the server:

```commandline
python ./src/main.py
```
The application will be available at `http://<host>:<port>`

## API Documentation
The API documentation is available at:
- Swagger UI: `http://<host>:<port>/docs`
- ReDoc: `http://<host>:<port>/redoc`