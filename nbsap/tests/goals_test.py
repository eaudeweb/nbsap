# encoding: utf-8
from common import _BaseTest

class GoalListingTest(_BaseTest):

    def test_goals_render_page(self):

        response = self.client.get('/goals')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock goal title", response.data)
        self.assertIn("btn-success", response.data)
        self.assertNotIn("btn-warning", response.data)

class GoalEditTest(_BaseTest):

    def test_goal_render_page(self):

        response = self.client.get('/goals/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_error_message_displayed_when_title_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "",
                    "body-en": "Some body text in english"
                 }

        response = self.client.post("/goals/1/edit", data=mydata)
        self.assertIn("Title is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            goals = [g for g in mongo.db.goals.find()]

        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]['title']['en'], 'Mock goal title')
        self.assertNotEqual(goals[0]['description']['en'], 'Some body text in english')

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Some title text in english",
                    "body-en": ""
                }

        response = self.client.post("/goals/1/edit", data=mydata)
        self.assertIn("Description is required", response.data)
        self.assertNotIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            goals = [g for g in mongo.db.goals.find()]

        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]['description']['en'], 'Mock goal description')
        self.assertNotEqual(goals[0]['title']['en'], 'Some title text in english')

    def test_error_message_missing_when_title_blank(self):

        mydata = {
                    "language": "fr",
                    "title-fr": "",
                    "body-fr": "some text in french"
                }

        response = self.client.post("/goals/1/edit", data=mydata)
        self.assertNotIn("Title is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            goals = [g for g in mongo.db.goals.find()]

        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]['description']['fr'], 'some text in french')
        self.assertEqual(goals[0]['title']['fr'], '')

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "sommige platte tekst in het Frans",
                    "body-nl": ""
                }

        response = self.client.post("/goals/1/edit", data=mydata)
        self.assertNotIn("Description is required", response.data)
        self.assertIn("Saved changes.", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            goals = [g for g in mongo.db.goals.find()]

        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]['title']['nl'], 'sommige platte tekst in het Frans')
        self.assertEqual(goals[0]['description']['nl'], '')

