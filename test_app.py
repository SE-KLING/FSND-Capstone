import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

AUTH_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3NjVCUGhIa1lfSmw2cDRKM3hjayJ9.eyJpc3MiOiJodHRwczovL25hbm9kYWNpdHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDVlOWZlNDI0ZWQ0MGJlZTM2Y2MxYyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTEwODc5OTEsImV4cCI6MTU5MTE1OTk5MCwiYXpwIjoiUjRVajg3YWdZWWp0dHdwcWYxbzlxeUIxWWpzZ0xneHAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Js9XIwZMHpWcCkifD3EmcvedtU6NPBHE8T5Zr70sLklWyLe-0aGYj61Y4ud1y_If0L0r98JnAyAFU6w1h_OupAcMPR2XEBMCDbb9tkh3dZp6NVVe1R5i-cIb3lEGpmkNa8IoYzt9O5xhvONfXftyz5UFfkHmCJfg7lZfO2Owxu6ix7vSa-Nii0xyz6ehSviXcujQDleE4vfrD1teg_KZeVGFZ_ifIIQgNaO-hF9nhBUgijpv7VSlqaN5aThCYsSKbPSzPaFYs3B_feuXv976VRndTNVicpbqJIuJ-tyEUlRfsoVPBEYU86iMCfsObQklylLdZDLgpzMWFe2ZQ6pKTQ'
AUTH_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3NjVCUGhIa1lfSmw2cDRKM3hjayJ9.eyJpc3MiOiJodHRwczovL25hbm9kYWNpdHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDVlOWQwMjY2MTRhMGJlNGI0MDEzNSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTEwODgxNzgsImV4cCI6MTU5MTE2MDE3NywiYXpwIjoiUjRVajg3YWdZWWp0dHdwcWYxbzlxeUIxWWpzZ0xneHAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.TG2BAiPx7xlXrFfZDX7MjHm2my2qCWVzRzbXmbYoiA63qAnR2gLfqougzMXaYYirQvxyaT3Zuey40RmA-l3hH2Flxoq08TlcHxL9iSZTqyk3pv2gu0H1Doc-Lv_I5aBCh_xJ_43i2c3alUF4-IuhbikMDEmmxrGhkIfsZM3WIa3Mh-TZOSX5mIdP5XJCyav_RAD0VFWJjLi1748pHsNNpdd7f6zXsmibNO7VZHDwCLNCEr_-P0qQVd3LuMX1oXSV9jWV2aHEWNp8_7auvtbZdxBWPQuE96x-TaP9QpFkMZzBYdI0Z99H-K4MiT9NvPKfPy9QQwIilmUf9AD9xwOrdQ'
AUTH_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3NjVCUGhIa1lfSmw2cDRKM3hjayJ9.eyJpc3MiOiJodHRwczovL25hbm9kYWNpdHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDVlOTZkNGUxYmM3MGJmMmYwOGFkYSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTEwODgzMTIsImV4cCI6MTU5MTE2MDMxMSwiYXpwIjoiUjRVajg3YWdZWWp0dHdwcWYxbzlxeUIxWWpzZ0xneHAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.j3WGLn1ggFwJBuDNxyz1Tr8u9v0MVIQowSMluxW-imp-CT4sgvd2OOVThrsFjaJisdLnjY6Q6E-qJzjcGker5_-6Wu2NF_emVgiEbjjhtCKrUWkj_1RYo3_1iqIBR8NJ3bcs_Ye24c9T5YXLHEMFKNbNXC--gn0H1EF6pz9MZ8aAips3zxpQ4kcKr35i3Ba7ntRPW_vVDzBBjTkcoBoCfo_UHuXiGnqYBkVNeTUJdnQ50bpKLkt6zY0m8EAak_My7y3Zra52XmYQjiFW5V_rfFGhpWvMvTNSliUYrM-l6RFLdcb5nFZcqqCsbv1GT-Bd5dQy3MJovnkoSqLzizgMPQ'


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
