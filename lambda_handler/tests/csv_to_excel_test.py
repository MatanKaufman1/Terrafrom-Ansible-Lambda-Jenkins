import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath("../csv_to_excel/"))
from csv_to_excel import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @patch("boto3.client")
    @patch("pandas.read_csv")
    @patch("pandas.ExcelWriter")
    @patch("os.remove")
    def test_successful_conversion(self, mock_remove, mock_excel_writer, mock_read_csv, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        mock_s3.download_file.side_effect = lambda bucket, key, filename: open(filename, "w").write("col1,col2\n1,2\n3,4")
        mock_s3.upload_file = MagicMock()

        mock_read_csv.return_value = MagicMock()

        mock_excel_writer.return_value = MagicMock()


        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {"name": "test-bucket"},
                        "object": {"key": "csv_files/test.csv"}
                    }
                }
            ]
        }


        lambda_handler(event, None)


        mock_s3.download_file.assert_called_once_with("test-bucket", "csv_files/test.csv", "/tmp/input.csv")
        mock_s3.upload_file.assert_called_once_with("/tmp/output.xlsx", "test-bucket", "excel_files/test.xlsx")
        mock_read_csv.assert_called_once_with("/tmp/input.csv")
        mock_excel_writer.assert_called_once_with("/tmp/output.xlsx")
        mock_remove.assert_any_call("/tmp/input.csv")
        mock_remove.assert_any_call("/tmp/output.xlsx")

if __name__ == "__main__":
    unittest.main()
