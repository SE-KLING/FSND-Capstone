import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

AUTH_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3NjVCUGhIa1lfSmw2cDRKM3hjayJ9.eyJpc3MiOiJodHRwczovL25hbm9kYWNpdHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDVlOWZlNDI0ZWQ0MGJlZTM2Y2MxYyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTExODM1NDAsImV4cCI6MTU5MTI1NTUzOSwiYXpwIjoiUjRVajg3YWdZWWp0dHdwcWYxbzlxeUIxWWpzZ0xneHAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.D6aotmdwZmHHRfz_2uvjR8vIPmwi-CTRXSJ2UIfqIU6I0Fl4cRBCVhXF9WAglPyVXPNYwyqNFI2xHfWOd3tssFsk5zbKT0rQigxQHzYRWy-PaVZxEJBv0E21XYLAtoTTOLWLa_RMum04nIloCzfVrlsfM56txKRQROFOy7tVaDp4MaGt5RrGngATaLESRHqOsNOWGuGa1X4uNH1elAAWKyUPiZy9ORYFSPYCAV6PtbCLBHmZZOo3HZnZRko0WaTWU06pHn14wCPgMczQze96Qb_ghZ9dGwgN60DOdvPVe7ar_-DHQob-QmG_9MleSRcVyZzxea0m9IzXIAlTWkZ9eQ'
AUTH_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3NjVCUGhIa1lfSmw2cDRKM3hjayJ9.eyJpc3MiOiJodHRwczovL25hbm9kYWNpdHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDVlOWQwMjY2MTRhMGJlNGI0MDEzNSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTExODM2NjEsImV4cCI6MTU5MTI1NTY2MCwiYXpwIjoiUjRVajg3YWdZWWp0dHdwcWYxbzlxeUIxWWpzZ0xneHAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.hB150fN2maIYb_OLB3i0MyAxIZaex9iEY3W-TwTTrJmnAklI_8K_J_DTdB60be8tIAwkOOA4s7KcvjKLSQJCzzmyhOG_y8-2V7YMNpqzf3sguD1r4vXR0AhJ4GkHudU5t4npPfirERZpbIBE-7JcflhoBgVMwyuNPc-qmWhC_utD99GRGrm6t4nP21uvr7UZNhcCRNM8TsHPpss5wyWi0Iz8Xs-Girrd2ZX2UovEB5BnYOTolyx7lP7GXY7tns7EUfJU-ZEtRk6pJXdMOsFHekpFpip1vfSMTqJB0J36qWZ0mA7sJXeWY1YJltv-wB68e9s3uJ-O_bLqcPwRZ46pwA'
AUTH_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3NjVCUGhIa1lfSmw2cDRKM3hjayJ9.eyJpc3MiOiJodHRwczovL25hbm9kYWNpdHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDVlOTZkNGUxYmM3MGJmMmYwOGFkYSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTExODM3NTEsImV4cCI6MTU5MTI1NTc1MCwiYXpwIjoiUjRVajg3YWdZWWp0dHdwcWYxbzlxeUIxWWpzZ0xneHAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.uXrtlZZvBnIshKgIKhw0w7Ya94AzrOgZl435QyxfKXMcV1-U5NyLu0LebsqwD4fSJCBggb5d-4ckUu7ZwlL6g8vrd2TAUVnTQUPX0-cDPyc22sLt5I-qdxPDYs9EQiqRg5G7cXhx6NVt3cQiOlM4BlIxEBP11ZPwljY_SYjBvJs5j2hlVa5OhYIerMn7QDD5Q32gAwF3l1yMAKexSu2W5XROsOMv1_jNK7My7yfyLwsRmdiceFeFbnJte3BjjJWn9ba-GQI_-PEPmKn7e1SF1KDQgP2Wgm4qcpWWNPwfnIWMR1BsknqBnVPUi9AkJIlSLkByhFmZqmJudJ9j_b-dpg'


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Initialize the app and define test variables"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting_agency'
        self.database_path = 'postgres://{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_name)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.actor_1 = {
            'name': 'Brad Pitt',
            'age': 54,
            'gender': 'male'
        }

        self.invalid_actor_1 = {
            'name': 'Brad Pitt',
            'age': 'Fifty-Four',
            'gender': 'male'
        }

        self.patch_actor_1 = {
            'name': 'Brad Pittt',
            'age': 37,
            'gender': 'male'
        }

        self.movie_1 = {
            'title': 'Once Upon a Time in Hollywood',
            'release_date': '2019-12-18',
            'actors': [1]
        }

        self.invalid_movie_1 = {
            'title': 'Once Upon a Time in Hollywood',
            'release_date': 'Date',
            'actors': [1]
        }

        self.patch_movie_1 = {
            'name': 'Once Upon a Time in Mexico',
            'release_date': '2019-12-18',
            'actors': [1]
        }

    # ----------------------------------------------------------------------------#
    # RBAC EXECUTIVE PRODUCER TESTS CREATE
    # ----------------------------------------------------------------------------#

    def test_create_actor_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().post('/actors', headers=headers, json=self.actor_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_create_movie_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().post('/movies', headers=headers, json=self.movie_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    # ----------------------------------------------------------------------------#
    # RBAC CASTING ASSISTANT TESTS
    # ----------------------------------------------------------------------------#

    def test_create_actor_403_assistant_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_ASSISTANT)}
        response = self.client().post('/movies', headers=headers, json=self.actor_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['description'], "Required permission not found")
        self.assertEqual(data['code'], "no_permission")

    def test_retrieve_actors_assistant_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_ASSISTANT)}
        response = self.client().get('/actors', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_retrieve_movies_assistant_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_ASSISTANT)}
        response = self.client().get('/movies', headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    # ----------------------------------------------------------------------------#
    # RBAC EXECUTIVE PRODUCER TESTS
    # ----------------------------------------------------------------------------#

    def test_create_actor_422_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().post('/actors', headers=headers, json=self.invalid_actor_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_create_movie_422_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().post('/movies', headers=headers, json=self.invalid_movie_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_retrieve_actors_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().get('/actors', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_retrieve_movies_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().get('/movies', headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_patch_actor_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().patch('/actors/1', headers=headers, json=self.patch_actor_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_patch_movie_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().patch('/movies/1', headers=headers, json=self.patch_movie_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_patch_actor_404_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().patch('/actors/100', json=self.patch_actor_1, headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_patch_movie_404_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().patch('/movies/100', json=self.patch_movie_1, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_delete_actor_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().delete('/actors/1', headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)

    def test_delete_movie_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().delete('/movies/1', headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 0)

    def test_delete_actor_404_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().delete('/actors/100', headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_delete_movie_404_producer_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_PRODUCER)}
        response = self.client().delete('/movies/100', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # ----------------------------------------------------------------------------#
    # RBAC CASTING DIRECTOR TESTS
    # ----------------------------------------------------------------------------#

    def test_create_movie_403_director_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_DIRECTOR)}
        response = self.client().post('/movies', headers=headers, json=self.movie_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['description'], "Required permission not found")
        self.assertEqual(data['code'], "no_permission")

    def test_create_actor_director_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_DIRECTOR)}
        response = self.client().post('/actors', headers=headers, json=self.actor_1)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_delete_actor_director_auth(self):
        headers = {"Authorization": "Bearer {}".format(AUTH_DIRECTOR)}
        response = self.client().delete('/actors/2', headers=headers)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)


class SequentialTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, test_case):
        test_names = super().getTestCaseNames(CastingAgencyTestCase)
        testcase_methods = list(CastingAgencyTestCase.__dict__.keys())
        test_names.sort(key=testcase_methods.index)
        return test_names


if __name__ == '__main__':
    unittest.main(testLoader=SequentialTestLoader())
