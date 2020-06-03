# Casting Agency API - Capstone Project

### Project Motivation
This project was created to act as an API backend for a Casting Agency. 
The project allows for CRUD actions concerning both actors and movies and allows for the streamlining of such management.

****

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

****

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

****

#### PIP Dependencies

Once you have your virtual environment set up and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

****

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

****

### Database Setup

Ensure you have Postgresql installed and running on your local machine
Create the Database by running the following in the terminal:
```
createdb casting
```

****

## Running the server

From within the current directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export DATABASE_URL='postgres://localhost:5432/casting'
export FLASK_APP=app.py
export FLASK_ENV=development
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

****

## API Endpoints

#### GET '/'
- Request Arguments: None
- Returns:
    - Acts as a health check and returns 'Welcome to the Casting Agency'
    
#### GET '/movies'
- Request Arguments: None
- Returns:
    - List of movies consisting of actor_ids, movie_id, release_date and title 
 ```
{
    "movies": [
        {
            "actors": [1],
            "id": 1,
            "release_date": "Wed, 18 Dec 2019 00:00:00 GMT",
            "title": "Once Upon a Time in Hollywood"
        }
    ],
    "success": true
}
```  
#### POST '/movies'
- Request Arguments: 
```
{
    "title": "Once Upon a Time in Hollywood",
    "release_date": "2019-12-18",
    "actors": [1]
}
```
- Returns:
    - List of movies consisting of actor_ids, movie_id, release_date and title, including the newly created movie
 ```
{
    "movies": [
        {
            "actors": [1],
            "id": 1,
            "release_date": "Wed, 18 Dec 2019 00:00:00 GMT",
            "title": "Once Upon a Time in Hollywood"
        }
    ],
    "success": true
}
``` 
#### PATCH '/movies/<int:movie_id>'
- Request Arguments:
    - A movie id must be passed in the URL
```
{
    "title": "Once Upon a Time in Mexico",
    "release_date": "2019-12-18",
    "actors": [1]
}
```
- Returns:
    - List of movies consisting of actor_ids, movie_id, release_date and title, including the newly updated movie
 ```
{
    "movies": [
        {
            "actors": [1],
            "id": 1,
            "release_date": "Wed, 18 Dec 2019 00:00:00 GMT",
            "title": "Once Upon a Time in Hollywood"
        }
    ],
    "success": true
}
``` 
#### DELETE '/movies/<int:movie_id>'
- Request Arguments: None. However, a movie id must be passed in the URL.
- Returns:
    - List of movies consisting of actor_ids, movie_id, release_date and title not including the deleted movie
 ```
{
    "movies": [
        {
            "actors": [1],
            "id": 1,
            "release_date": "Wed, 18 Dec 2019 00:00:00 GMT",
            "title": "Once Upon a Time in Hollywood"
        }
    ],
    "success": true
}
``` 
#### GET '/actors'
- Request Arguments: None
- Returns:
    - List of actors consisting of actor age, gender, name and id 
 ```
{
    "actors": [
        {
            "age": 54,
            "gender": "male",
            "id": 1,
            "name": "Brad Pitt"
        }
    ],
    "success": true
}
```  
#### POST '/actors'
- Request Arguments: 
```
{
    'name': 'Brad Pitt',
    'age': 54,
    'gender': 'male'
}
```
- Returns:
    - List of actors consisting of actor age, gender, name and id, including newly created actor
 ```
{
    "actors": [
        {
            "age": 54,
            "gender": "male",
            "id": 1,
            "name": "Brad Pitt"
        }
    ],
    "success": true
}
``` 
#### PATCH '/actors/<int:actor_id>'
- Request Arguments:
    - An actor id must be passed in the URL 
```
{
    'name': 'Brad Pitttttt',
    'age': 54,
    'gender': 'male'
}
```
- Returns:
    - - List of actors consisting of actor age, gender, name and id, including newly updated actor
 ```
{
    "actors": [
        {
            "age": 54,
            "gender": "male",
            "id": 1,
            "name": "Brad Pittttt"
        }
    ],
    "success": true
}
``` 
#### DELETE '/actors/<int:actor_id>'
- Request Arguments: None. However, an actor id must be passed in the URL.
- Returns:
    - List of actors consisting of actor_ids, movie_id, release_date and title not including the deleted movie
 ```
{
    "movies": [
        {
            "actors": [1],
            "id": 1,
            "release_date": "Wed, 18 Dec 2019 00:00:00 GMT",
            "title": "Once Upon a Time in Hollywood"
        }
    ],
    "success": true
}
``` 

****

## Authentication

The project also allows for users with different roles and privileges, namely:

#### Casting Assistant: 
- Permissions: Ability to view actors and movies.
#### Casting Director:
- Permissions: Includes Casting Assistant permissions as well as being able to create and delete actors and edit movies
#### Executive Producer: 
- Permissions: Includes Casting Director permissions as well as being able to create an delete movies

****

## Testing Application
In order to run tests run the following commands: 

```
$ dropdb casting
$ createdb casting
$ python test_app.py
```

The first time you run the tests, omit the dropdb command and also uncomment `db.create_all()` which is located in the 
`models.py` file of the project.

## Accessing Application
- The application hosted by heroku can be accessed [here](https://nano-casting-agency.herokuapp.com)
- Please note the JWT Tokens for the different roles mentioned above can be found in ```test_app.py``` and should be included in requests.
- If JWT tokens are expired you can create new ones by logging in at [this](https://nanodacity.auth0.com/authorize?audience=casting&response_type=token&client_id=R4Uj87agYYjttwpqf1o9qyB1YjsgLgxp&redirect_uri=http://127.0.0.1:8080) URL 
- Use the following credentials for different roles 
    - Casting Assistant: ```email``` = assistant@udacity.com | ```password``` = Udacity@123
    - Casting Director: ```email``` = director@udacity.com | ```password``` = Udacity@123
    - Executive Producer: ```email``` = producer@udacity.com | ```password``` = Udacity@123
