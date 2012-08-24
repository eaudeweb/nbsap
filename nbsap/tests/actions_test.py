# encoding: utf-8
from common import _BaseTest

class ObjectiveEditTest(_BaseTest):

    def test_render_page(self):
        response = self.client.get('/objectives/1/1/action')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "body-en": ""
                }
        response = self.client.post("/objectives/1/1/action/edit", data=mydata)
        html = response.data
        self.assertIn("Body is required", html)
        self.assertNotIn("Saved changes.", html)

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "body-nl": ""
                }
        response = self.client.post("/objectives/1/1/action/edit", data=mydata)
        html = response.data
        self.assertNotIn("English is required", html)
        self.assertIn("Saved changes.", html)

