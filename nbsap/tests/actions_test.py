# encoding: utf-8
from common import _BaseTest

class ActionEditTest(_BaseTest):

    def test_render_page(self):

        response = self.client.get('/admin/objectives/1/action/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/admin/objectives/1/action/2')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Testing 1,2,3",
                    "body-en": ""
                }

        response = self.client.post("/admin/objectives/1/action/1/edit", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            actions = [a for a in objective['actions']]

        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['body']['en'], \
                                    'Mock body action in subobjective')

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "Limit test",
                    "body-nl": ""
                }

        response = self.client.post("/admin/objectives/1/action/1/edit", data=mydata)
        self.assertNotIn("Description is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objective = mongo.db.objectives.find_one_or_404({'id': 1})
            actions = [a for a in objective['actions']]

        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['title']['nl'], "Limit test")
        self.assertEqual(actions[0]['body']['nl'], "")
