import os
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath("../create_project/"))
from create_project import lambda_handler, create_gitlab_project, upload_file_to_gitlab


class TestLambdaHandler(unittest.TestCase):

    @patch("create_project.create_gitlab_project")
    @patch("create_project.upload_file_to_gitlab")
    def test_lambda_handler_success(self, mock_upload_file_to_gitlab, mock_create_gitlab_project):
        # Mock create_gitlab_project to return a fake project
        mock_create_gitlab_project.return_value = {"id": 12345}

        # Mock upload_file_to_gitlab to simulate successful file upload
        mock_upload_file_to_gitlab.return_value = {"file_path": "main.py"}

        # Simulated event
        event = {
            "project_name": "test-project",
            "suffix": "py"
        }

        # Call the Lambda handler
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response['statusCode'], 200)
        self.assertIn("Project test-project created and file main.py uploaded to GitLab.", response['body'])

        # Ensure the mocks were called with the correct parameters
        mock_create_gitlab_project.assert_called_once_with("test-project")
        mock_upload_file_to_gitlab.assert_called_once_with(12345, "main.py", "")

    def test_lambda_handler_missing_parameters(self):
        # Simulated event with missing parameters
        event = {}

        # Call the Lambda handler
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response['statusCode'], 400)
        self.assertIn("Project name and suffix are required", response['body'])

    def test_lambda_handler_invalid_suffix(self):
        # Simulated event with an invalid suffix
        event = {
            "project_name": "test-project",
            "suffix": "invalid_suffix"
        }

        # Call the Lambda handler
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response['statusCode'], 400)
        self.assertIn("Invalid suffix", response['body'])

    @patch("create_project.create_gitlab_project")
    @patch("create_project.upload_file_to_gitlab")
    def test_lambda_handler_exception(self, mock_upload_file_to_gitlab, mock_create_gitlab_project):
        # Mock create_gitlab_project to raise an exception
        mock_create_gitlab_project.side_effect = Exception("GitLab API error")

        # Simulated event
        event = {
            "project_name": "test-project",
            "suffix": "py"
        }

        # Call the Lambda handler
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response['statusCode'], 500)
        self.assertIn("GitLab API error", response['body'])


if __name__ == "__main__":
    unittest.main()
