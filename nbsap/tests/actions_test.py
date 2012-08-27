# encoding: utf-8
from common import _BaseTest

class ActionEditTest(_BaseTest):

    def test_render_page(self):

        response = self.client.get('/objectives/1/1/action')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "body-en": ""
                }

        response = self.client.post("/objectives/1/1/action/edit", data=mydata)
        self.assertIn("Body is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            actions = [a for a in mongo.db.actions.find()]

        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]['actions'][0]['body']['en'], \
                                    'Mock body action in subobjective')

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "body-nl": ""
                }

        response = self.client.post("/objectives/1/1/action/edit", data=mydata)
        self.assertNotIn("Body is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            actions = [a for a in mongo.db.actions.find()]

        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]['actions'][0]['body']['nl'], '')

