from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from auth import AuthError, requires_auth
from models import setup_db, db, Movie, Actor

app = Flask(__name__)


def create_app(test_config=None):
    # configure app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/')
    def index():
        try:
            return "Welcome to the Casting Agency"
        except Exception:
            abort(500)

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    # ----------------------------------------------------------------------------#
    # MOVIE ROUTES.
    # ----------------------------------------------------------------------------#

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        """
        Returns a list of all available Movies from Database
        """
        movies = Movie.query.order_by(Movie.id).all()
        if not movies:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
                "success": True,
                "movies": formatted_movies
            })

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def create_movie(payload):
        """
        Allows for creation of movies
        """
        body = request.get_json()
        try:
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            actors = Actor.query.filter(Actor.id.in_(body.get('actors', None))).all()

            movie = Movie(title=title, release_date=release_date)
            movie.actors = actors
            movie.insert()

            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        """
        Allows a movie to be updated
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()

        try:
            movie.title = body.get('title', None)
            movie.release_date = body.get('release_date', None)
            movie.actors = Actor.query.filter(Actor.id.in_(body.get('actors', None))).all()
            movie.update()

            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        """
        Allows a movie to be deleted
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except Exception:
            abort(422)

    # ----------------------------------------------------------------------------#
    # ACTOR ROUTES.
    # ----------------------------------------------------------------------------#

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        """
        Returns a list of all available Actors from Database
        """
        actors = Actor.query.order_by(Actor.id).all()
        if not actors:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
                "success": True,
                "actors": formatted_actors
            })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        """
        Allows for creation of actors
        """
        body = request.get_json()
        try:
            name = body.get('name', None)
            gender = body.get('gender', None)
            age = body.get('age', None)

            actor = Actor(name=name, gender=gender, age=age)
            actor.insert()

            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        """
        Allows for editing of actors
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()

        try:
            actor.name = body.get('name', None)
            actor.gender = body.get('gender', None)
            actor.age = body.get('age', None)
            actor.update()

            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        """
        Allows an actor to be deleted
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            actor.delete()
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)

    # ----------------------------------------------------------------------------#
    # ERROR HANDLING.
    # ----------------------------------------------------------------------------#
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": error.status_code,
            "code": error.error["code"],
            "description": error.error["description"]
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
