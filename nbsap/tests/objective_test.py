# encoding: utf-8
from common import _BaseTest

class ObjectiveListingTest(_BaseTest):

     def test_objectives_render_page(self):

        response = self.client.get('/objectives')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock objective title", response.data)
        self.assertIn("btn-success", response.data)
        self.assertNotIn("btn-warning", response.data)

class ObjectiveEditTest(_BaseTest):

    def test_objective_render_page(self):

        response = self.client.get('/objectives/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_title_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "",
                    "body-en": "Some body text in english"
                 }

        response = self.client.post("/objectives/1/edit", data=mydata)
        self.assertIn("Title is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['title']['en'], 'Mock objective title')
        self.assertNotEqual(objectives[0]['body']['en'], 'Some body text in english')

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Some title text in english",
                    "body-en": ""
                }

        response = self.client.post("/objectives/1/edit", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['body']['en'], 'Mock objective body')
        self.assertNotEqual(objectives[0]['title']['en'], 'Some title text in english')

    def test_error_message_missing_when_title_blank(self):

        mydata = {
                    "language": "fr",
                    "title-fr": "",
                    "body-fr": "some text in french"
                }

        response = self.client.post("/objectives/1/edit", data=mydata)
        self.assertNotIn("Title is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['body']['fr'], 'some text in french')
        self.assertEqual(objectives[0]['title']['fr'], '')


    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "sommige platte tekst in het Frans",
                    "body-nl": ""
                }

        response = self.client.post("/objectives/1/edit", data=mydata)
        self.assertNotIn("Body is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            objectives = [o for o in mongo.db.objectives.find()]

        self.assertEqual(len(objectives), 1)
        self.assertEqual(objectives[0]['body']['nl'], '')
        self.assertEqual(objectives[0]['title']['nl'], 'sommige platte tekst in het Frans')

