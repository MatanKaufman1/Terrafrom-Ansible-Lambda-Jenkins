import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath("../get_info/"))
from get_info import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @patch("boto3.client")
    @patch("wikipediaapi.Wikipedia")
    def test_successful_execution(self, mock_wikipedia, mock_boto3_client):
        # Mock S3 client
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Mock S3 download to create a temp file with content
        mock_s3.download_file.side_effect = lambda bucket, key, filename: open(filename, "w").write("Sharon and Matan")

        # Mock Wikipedia API to return a page summary
        mock_page = MagicMock()
        mock_page.exists.return_value = True
        mock_page.summary = "Sharon and Matan are great."
        mock_wikipedia.return_value.page.return_value = mock_page

        # Simulate event
        event = {
            "Records": [
                {"s3": {"bucket": {"name": "bucket-matan"}, "object": {"key": "wikipedia_files/example.txt"}}}
            ]
        }

        # Run the Lambda function
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Successfully appended summary", response["body"])

    @patch("boto3.client")
    def test_missing_subject(self, mock_boto3_client):
        # Mock S3 client
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Mock S3 download to create an empty file
        mock_s3.download_file.side_effect = lambda bucket, key, filename: open(filename, "w").write("")

        # Simulate event
        event = {
            "Records": [
                {"s3": {"bucket": {"name": "bucket-matan"}, "object": {"key": "wikipedia_files/empty.txt"}}}
            ]
        }

        # Run the Lambda function
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Error: Subject is missing", response["body"])

if __name__ == "__main__":
    unittest.main()
