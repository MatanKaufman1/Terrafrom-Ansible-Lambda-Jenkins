import os
import boto3
import pandas as pd


def lambda_handler(event, context):
    """
    AWS Lambda function to convert a CSV file in S3 to Excel format and save it back to S3.
    Args:
        event (dict): The S3 event payload.
        context (object): Lambda context runtime methods and attributes.
    """
    try:
        # Extract bucket name and file key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        csv_key = event['Records'][0]['s3']['object']['key']

        # Construct the Excel file key
        excel_key = csv_key.replace('csv_files/', 'excel_files/').replace('.csv', '.xlsx')
        # excel_key = "Corona.xlsx"

        # Temporary file paths for processing
        local_csv_path = '/tmp/input.csv'
        local_excel_path = '/tmp/output.xlsx'

        # Initialize S3 client
        s3_client = boto3.client('s3')

        # Download the CSV file from S3
        print(f"Downloading {csv_key} from bucket {bucket_name}...")
        s3_client.download_file(bucket_name, csv_key, local_csv_path)

        # Convert the CSV file to Excel format
        print(f"Converting {csv_key} to Excel format...")
        df = pd.read_csv(local_csv_path)
        with pd.ExcelWriter(local_excel_path) as excel_writer:
            df.to_excel(excel_writer, index=False)

        # Upload the Excel file back to S3
        print(f"Uploading {excel_key} to bucket {bucket_name}...")
        s3_client.upload_file(local_excel_path, bucket_name, excel_key)

        # Clean up temporary files
        os.remove(local_csv_path)
        os.remove(local_excel_path)

        print(f"Successfully converted {csv_key} to {excel_key} in bucket {bucket_name}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    # sharon and matan