from django.test import TestCase
from unittest.mock import patch
import os

from . import nlp_engine
from .weather_bot import get_weather_info
from .ai_buddy import sendEmail


class NLUTests(TestCase):
    def test_weather_entity_extraction(self):
        parsed = nlp_engine.parse_input('what is the weather in Paris')
        self.assertEqual(parsed['intent'], 'weather')
        self.assertIn('city', parsed['entities'])
        self.assertEqual(parsed['entities']['city'], 'paris')


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
