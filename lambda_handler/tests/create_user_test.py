import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath("../create_user/"))

from create_user import create_gitlab_user


class TestCreateGitLabUser(unittest.TestCase):

    @patch("create_user.requests.post")  
    def test_create_gitlab_user_success(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123}
        mock_post.return_value = mock_response


        user_id = create_gitlab_user(username="testuser", email="test@example.com", password="securepassword")


        self.assertEqual(user_id, 123)
        mock_post.assert_called_once_with(
            "http://3.126.51.24:80/api/v4/users",
            headers={"Authorization": "Bearer None"},  #
            json={
                "name": "testuser",
                "username": "testuser",
                "email": "test@example.com",
                "password": "securepassword",
                "skip_confirmation": True
            }
        )

    @patch("create_user.requests.post")
    def test_create_gitlab_user_failure(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad Request"}
        mock_post.return_value = mock_response

        user_id = create_gitlab_user(username="testuser", email="test@example.com", password="securepassword")


        self.assertIsNone(user_id)
        mock_post.assert_called_once()

    @patch("create_user.requests.post")
    def test_create_gitlab_user_exception(self, mock_post):

        mock_post.side_effect = Exception("Network error")


        user_id = create_gitlab_user(username="testuser", email="test@example.com", password="securepassword")

        self.assertIsNone(user_id)
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
