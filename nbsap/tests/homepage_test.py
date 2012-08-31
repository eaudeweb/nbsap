# encoding: utf-8
from common import _BaseTest

class HomepageTest(_BaseTest):

    def test_render_pages(self):

        self.assertEqual(self.client.get('/homepage').status_code, 302)
        self.assertEqual(self.client.get('/homepage/goals').status_code, 200)
        self.assertEqual(self.client.get('/homepage/indicators').status_code, 200)
        self.assertEqual(self.client.get('/homepage/objectives').status_code, 200)

        self.assertEqual(self.client.get('/homepage/goals/B').status_code, 404)
        self.assertEqual(self.client.get('/homepage/indicators?page=6').status_code, 404)
        self.assertEqual(self.client.get('/homepage/objectives/2').status_code, 404)
