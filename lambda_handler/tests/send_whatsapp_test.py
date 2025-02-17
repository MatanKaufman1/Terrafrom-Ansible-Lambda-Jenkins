import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath("../send_whatsapp/"))

from send_whatsapp import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch("send_whatsapp.Client")  
    @patch.dict("os.environ", {"ACCOUNT_SID": "test_sid", "TWILLO_TOKEN": "test_token"})  #
    def test_message_sent_successfully(self, mock_twilio_client):

        mock_client_instance = MagicMock()
        mock_twilio_client.return_value = mock_client_instance
        mock_message = MagicMock()
        mock_message.sid = "test_message_sid"
        mock_client_instance.messages.create.return_value = mock_message


        event = {
            "phone": "503456787",  
            "message": "Hello, this is a test message"
        }


        response = lambda_handler(event, None)


        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Message sent successfully", response["body"])


        mock_client_instance.messages.create.assert_called_once_with(
            from_='whatsapp:+14155238886',
            body="Hello, this is a test message",
            to="whatsapp:+972503456789"
        )


    @patch("send_whatsapp.Client")  
    @patch.dict("os.environ", {"ACCOUNT_SID": "test_sid", "TWILLO_TOKEN": "test_token"})  # Mock environment variables
    def test_twilio_exception(self, mock_twilio_client):

        mock_client_instance = MagicMock()
        mock_twilio_client.return_value = mock_client_instance
        mock_client_instance.messages.create.side_effect = Exception("Twilio error")


        event = {
            "phone": "503456789",
            "message": "Hello, this is a test message"
        }

        response = lambda_handler(event, None)


        self.assertEqual(response["statusCode"], 500)
        self.assertIn("An error occurred", response["body"])


if __name__ == "__main__":
    unittest.main()
