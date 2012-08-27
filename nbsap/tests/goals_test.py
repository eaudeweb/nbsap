# encoding: utf-8
from common import _BaseTest

class GoalEditTest(_BaseTest):

    def test_goals_render_page(self):
        response = self.client.get('/goals')
        self.assertEqual(response.status_code, 200)

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
        html = response.data
        self.assertIn("Title is required", html)
        self.assertNotIn("Saved changes.", html)

    def test_error_message_displayed_when_body_blank(self):

        mydata = {
                    "language": "en",
                    "title-en": "Some title text in english",
                    "body-en": ""
                }
        response = self.client.post("/goals/1/edit", data=mydata)
        html = response.data
        self.assertIn("Description is required", html)
        self.assertNotIn("Saved changes.", html)


    def test_error_message_missing_when_title_blank(self):

        mydata = {
                    "language": "fr",
                    "title-fr": "",
                    "body-fr": "certains corps de texte en français"
                }
        response = self.client.post("/goals/1/edit", data=mydata)
        html = response.data

        self.assertNotIn("Title is required", html)
        self.assertIn("Saved changes.", html)

    def test_error_message_missing_when_body_blank(self):

        mydata = {
                    "language": "nl",
                    "title-nl": "sommige platte tekst in het Frans",
                    "body-nl": ""
                }
        response = self.client.post("/objectives/1/edit", data=mydata)
        html = response.data
        self.assertNotIn("Description is required", html)
        self.assertIn("Saved changes.", html)
