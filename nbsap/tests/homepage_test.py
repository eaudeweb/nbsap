# encoding: utf-8
from common import _BaseTest

class HomepageTest(_BaseTest):

    def test_render_pages(self):

        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/goals').status_code, 200)
        self.assertEqual(self.client.get('/indicators').status_code, 200)
        self.assertEqual(self.client.get('/objectives').status_code, 200)

        self.assertEqual(self.client.get('/goals/B').status_code, 404)
        self.assertEqual(self.client.get('/indicators?page=6').status_code, 404)
        self.assertEqual(self.client.get('/objectives/2').status_code, 404)
