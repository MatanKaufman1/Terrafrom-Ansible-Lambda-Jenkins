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

        mock_create_gitlab_project.return_value = {"id": 12345}


        mock_upload_file_to_gitlab.return_value = {"file_path": "main.py"}


        event = {
            "project_name": "test-project",
            "suffix": "py"
        }
        response = lambda_handler(event, None)


        self.assertEqual(response['statusCode'], 200)
        self.assertIn("Project test-project created and file main.py uploaded to GitLab.", response['body'])


        mock_create_gitlab_project.assert_called_once_with("test-project")
        mock_upload_file_to_gitlab.assert_called_once_with(12345, "main.py", "")

    def test_lambda_handler_missing_parameters(self):

        event = {}


        response = lambda_handler(event, None)


        self.assertEqual(response['statusCode'], 400)
        self.assertIn("Project name and suffix are required", response['body'])

    def test_lambda_handler_invalid_suffix(self):
        event = {
            "project_name": "test-project",
            "suffix": "invalid_suffix"
        }

        response = lambda_handler(event, None)


        self.assertEqual(response['statusCode'], 400)
        self.assertIn("Invalid suffix", response['body'])

    @patch("create_project.create_gitlab_project")
    @patch("create_project.upload_file_to_gitlab")
    def test_lambda_handler_exception(self, mock_upload_file_to_gitlab, mock_create_gitlab_project):
        mock_create_gitlab_project.side_effect = Exception("GitLab API error")


        event = {
            "project_name": "test-project",
            "suffix": "py"
        }


        response = lambda_handler(event, None)


        self.assertEqual(response['statusCode'], 500)
        self.assertIn("GitLab API error", response['body'])


if __name__ == "__main__":
    unittest.main()
