import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath("../send_whatsapp/"))

from send_whatsapp import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch("send_whatsapp.Client")  # Mock Twilio Client
    @patch.dict("os.environ", {"ACCOUNT_SID": "test_sid", "TWILLO_TOKEN": "test_token"})  # Mock environment variables
    def test_message_sent_successfully(self, mock_twilio_client):
        # Mock Twilio client and message creation
        mock_client_instance = MagicMock()
        mock_twilio_client.return_value = mock_client_instance
        mock_message = MagicMock()
        mock_message.sid = "test_message_sid"
        mock_client_instance.messages.create.return_value = mock_message

        # Simulated event
        event = {
            "phone": "503456789",  # Example phone number
            "message": "Hello, this is a test message"
        }

        # Call the Lambda handler
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Message sent successfully", response["body"])

        # Verify Twilio client interactions
        mock_client_instance.messages.create.assert_called_once_with(
            from_='whatsapp:+14155238886',
            body="Hello, this is a test message",
            to="whatsapp:+972503456789"
        )


    @patch("send_whatsapp.Client")  # Mock Twilio Client
    @patch.dict("os.environ", {"ACCOUNT_SID": "test_sid", "TWILLO_TOKEN": "test_token"})  # Mock environment variables
    def test_twilio_exception(self, mock_twilio_client):
        # Mock Twilio client to raise an exception
        mock_client_instance = MagicMock()
        mock_twilio_client.return_value = mock_client_instance
        mock_client_instance.messages.create.side_effect = Exception("Twilio error")

        # Simulated event
        event = {
            "phone": "503456789",
            "message": "Hello, this is a test message"
        }
        # Call the Lambda handler
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response["statusCode"], 500)
        self.assertIn("An error occurred", response["body"])


if __name__ == "__main__":
    unittest.main()
