from django.test import TestCase
from unittest.mock import patch
import os
import json

from . import nlp_engine
from .weather_bot import get_weather_info
from .ai_buddy import process_input, sendEmail


class NLUTests(TestCase):
    def test_weather_entity_extraction(self):
        parsed = nlp_engine.parse_input('what is the weather in Paris')
        self.assertEqual(parsed['intent'], 'weather')
        self.assertIn('city', parsed['entities'])
        self.assertEqual(parsed['entities']['city'], 'paris')

    @patch('tenali.nlp_engine._predict_intent_with_model', return_value=('weather', 0.99))
    def test_destructive_intents_take_precedence_over_model_predictions(self, predict):
        parsed = nlp_engine.parse_input('shut down the system')

        self.assertEqual(parsed['intent'], 'shutdown')


class NLUTrainingTests(TestCase):
    def test_intent_data_loads_and_converts(self):
        from tenali.ml_models.training import train_nlu
        texts, intents = train_nlu.load_intent_data()
        self.assertTrue(len(texts) > 0)
        self.assertTrue(len(intents) > 0)
        examples, labels = train_nlu.convert_to_spacy_format(texts, intents)
        self.assertTrue(len(examples) > 0)
        self.assertTrue(len(labels) > 0)


class WeatherTests(TestCase):
    def test_weather_without_api_key_returns_message(self):
        # Ensure OPENWEATHER_API_KEY is not set
        with patch.dict(os.environ, {}, clear=True):
            msg = get_weather_info('weather in London')
            self.assertIn('Weather API key not configured', msg)


class EmailTests(TestCase):
    def test_send_email_without_creds_returns_not_configured(self):
        # Patch speak to avoid TTS side effects
        with patch.dict(os.environ, {}, clear=True):
            with patch('tenali.actuators.speak') as mock_speak:
                result = sendEmail('foo@example.com', 'hello')
                self.assertEqual(result, 'EmailNotConfigured')

    @patch('tenali.ai_buddy.speak')
    @patch('tenali.ai_buddy.sendEmail', return_value='EmailFailed')
    @patch('tenali.ai_buddy.parse_input', return_value={'intent': 'send_email', 'entities': {}})
    def test_email_failure_is_not_reported_as_success(self, parse, send_email, speak):
        response = process_input('send email to foo@example.com saying hello')

        self.assertIn('could not be sent', response)
        self.assertNotIn('successfully', response)
        send_email.assert_called_once_with('foo@example.com', 'hello')

    @patch('tenali.ai_buddy.speak')
    @patch('tenali.ai_buddy.sendEmail', return_value='EmailSent')
    @patch('tenali.ai_buddy.parse_input', return_value={'intent': 'send_email', 'entities': {}})
    def test_email_success_is_reported_only_after_success_status(self, parse, send_email, speak):
        response = process_input('send email to foo@example.com saying hello')

        self.assertEqual(response, 'Email sent successfully.')

    @patch('tenali.ai_buddy.smtplib.SMTP')
    @patch('tenali.ai_buddy.speak')
    @patch.dict(os.environ, {'EMAIL_USER': 'sender@example.com', 'EMAIL_PASS': 'secret'})
    def test_refused_email_recipient_returns_failure(self, speak, smtp):
        smtp.return_value.__enter__.return_value.sendmail.return_value = {
            'foo@example.com': (550, b'No such recipient')
        }

        self.assertEqual(sendEmail('foo@example.com', 'hello'), 'EmailFailed')


class HomeViewTests(TestCase):
    def post_json(self, payload):
        return self.client.post(
            '/home/',
            data=json.dumps(payload),
            content_type='application/json',
        )

    @patch('tenali.views.process_input', return_value='Hello')
    def test_home_processes_browser_supplied_text(self, process):
        response = self.post_json({'text': 'hello'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_input'], 'hello')
        process.assert_called_once_with('hello')

    def test_home_rejects_empty_or_invalid_payload(self):
        empty_text = self.post_json({'text': '  '})
        malformed_json = self.client.post(
            '/home/',
            data='{',
            content_type='application/json',
        )

        self.assertEqual(empty_text.status_code, 400)
        self.assertEqual(malformed_json.status_code, 400)

    @patch('tenali.views.execute_system_action', return_value='Shutting down')
    def test_system_action_requires_valid_confirmation_and_is_one_time(self, execute):
        request = self.post_json({'text': 'shut down the system'})
        request_data = request.json()
        token = request_data['confirmation_token']

        self.assertEqual(request.status_code, 200)
        self.assertTrue(request_data['confirmation_required'])
        execute.assert_not_called()

        confirmed = self.post_json({'confirmation_token': token, 'confirm': True})
        repeated = self.post_json({'confirmation_token': token, 'confirm': True})

        self.assertEqual(confirmed.status_code, 200)
        self.assertEqual(confirmed.json()['response'], execute.return_value)
        self.assertEqual(repeated.status_code, 400)
        execute.assert_called_once_with('shutdown')

    @patch('tenali.views.execute_system_action')
    def test_canceling_system_action_does_not_execute_it(self, execute):
        request = self.post_json({'text': 'restart the system'})
        canceled = self.post_json({
            'confirmation_token': request.json()['confirmation_token'],
            'confirm': False,
        })

        self.assertEqual(canceled.status_code, 200)
        self.assertEqual(canceled.json()['response'], 'System action canceled.')
        execute.assert_not_called()

    def test_confirmation_token_expires(self):
        request = self.post_json({'text': 'restart the system'})
        token = request.json()['confirmation_token']
        session = self.client.session
        pending = session['pending_destructive_action']
        pending['created_at'] = 0
        session['pending_destructive_action'] = pending
        session.save()

        response = self.post_json({'confirmation_token': token, 'confirm': True})

        self.assertEqual(response.status_code, 400)
        self.assertIn('expired', response.json()['error'])

    def test_home_post_requires_csrf_token(self):
        from django.test import Client

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.get('/home/')

        response = csrf_client.post(
            '/home/',
            data=json.dumps({'text': 'hello'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 403)
