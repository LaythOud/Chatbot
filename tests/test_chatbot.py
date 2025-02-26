import unittest
from flask import json
from src import create_app

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_chat_handler(self):
        response = self.client.post('/chatbot/chat', json={'message': 'Hello'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', data)

    def test_reset_context(self):
        response = self.client.post('/chatbot/reset')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'context reset')

if __name__ == '__main__':
    unittest.main()
