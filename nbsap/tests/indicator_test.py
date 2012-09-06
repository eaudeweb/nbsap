# encoding: utf-8
from common import _BaseTest

class IndicatorListingTest(_BaseTest):

     def test_indicators_render_page(self):

        response = self.client.get('/admin/indicators')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mock indicator name", response.data)
        self.assertIn("btn-success", response.data)
        self.assertNotIn("btn-warning", response.data)

class IndicatorEditTest(_BaseTest):

    def test_indicator_render_page(self):

        response = self.client.get('/admin/indicators/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_successfully_edited(self):

        data = {
                    'language': 'en',
                    'goal': 'B',
                    'name_en': 'New indicator name',
                    'question_en': 'New question',
                    'head_indicator_en': 'New head indicator',
                    'sub_indicator_en': 'New sub indicator',
                    'classification_en': 'New classification',
                    'status_en': 'New status',
                    'sources_en': 'New sources',
                    'requirements_en': 'New requirements',
                    'measurer_en': 'New measurer',
                    'relevant_target': '5',
                    'other_targets': ['1', '2'],
                    'sensitivity': 'High',
                    'ease_of_communication': 'High',
                    'validity': '',
                    'scale': ['G', 'N'],
                    'conventions': 'New indicator conventions',
                    'url_name_en_0': 'New link name',
                    'url_0': 'New link'
                }

        response = self.client.post("/admin/indicators/1/edit", data=data)
        self.assertIn("Saved changes", response.data)

        from nbsap.database import mongo
        with self.app.test_request_context():
            indicators = [i for i in mongo.db.indicators.find()]

        self.assertEqual(len(indicators), 1)
        self.assertEqual(indicators[0]['id'], 1)

        self.assertEqual(indicators[0]['name']['en'], 'New indicator name')
        self.assertEqual(indicators[0]['question']['en'], 'New question')
        self.assertEqual(indicators[0]['head_indicator']['en'], 'New head indicator')
        self.assertEqual(indicators[0]['sub_indicator']['en'], 'New sub indicator')
        self.assertEqual(indicators[0]['classification']['en'], 'New classification')
        self.assertEqual(indicators[0]['status']['en'], 'New status')
        self.assertEqual(indicators[0]['sources']['en'], 'New sources')
        self.assertEqual(indicators[0]['requirements']['en'], 'New requirements')
        self.assertEqual(indicators[0]['measurer']['en'], 'New measurer')
        self.assertEqual(indicators[0]['goal'], 'B')
        self.assertEqual(indicators[0]['relevant_target'], '5')
        self.assertEqual(indicators[0]['other_targets'], ['1', '2'])
        self.assertEqual(indicators[0]['sensitivity'], 'High')
        self.assertEqual(indicators[0]['ease_of_communication'], 'High')
        self.assertEqual(indicators[0]['validity'], None)
        self.assertEqual(indicators[0]['scale'], ['G', 'N'])
        self.assertEqual(indicators[0]['conventions'], 'New indicator conventions')
        self.assertEqual(len(indicators[0]['links']), 1)
        self.assertEqual(indicators[0]['links'][0]['url_name']['en'], 'New link name')
        self.assertEqual(indicators[0]['links'][0]['url'], 'New link')

