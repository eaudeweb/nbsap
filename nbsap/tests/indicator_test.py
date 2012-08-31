# encoding: utf-8
from common import _BaseTest

class IndicatorListingTest(_BaseTest):

     def test_indicators_render_page(self):

        response = self.client.get('/indicators')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock indicator name", response.data)
        self.assertIn("btn-success", response.data)
        self.assertNotIn("btn-warning", response.data)
