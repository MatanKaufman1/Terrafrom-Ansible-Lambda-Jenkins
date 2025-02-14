import os
import boto3
import datetime

S3_BUCKET_NAME = 'bucket-matan'
BACKUP_PREFIX = 'backup_files/'
DAILY_BACKUP_PREFIX = 'daily_backups/'
WEEKLY_BACKUP_PREFIX = 'weekly_backups/'
MONTHLY_BACKUP_PREFIX = 'monthly_backups/'

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        today = datetime.date.today()
        day_of_week = today.weekday()
        first_day_of_month = today.day == 1

        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=BACKUP_PREFIX)
        if 'Contents' not in response:
            print("No files to backup.")
            return {"statusCode": 200, "body": "No files to backup"}

        files = response['Contents']
        print(f"Found {len(files)} files to backup.")

        # Iterate over files and create daily backups
        for file in files:
            file_key = file['Key']
            file_name = os.path.basename(file_key)
            today_backup_key = f"{DAILY_BACKUP_PREFIX}{today}/{file_name}"

            # Copy to daily backup location
            s3_client.copy_object(
                Bucket=S3_BUCKET_NAME,
                CopySource={'Bucket': S3_BUCKET_NAME, 'Key': file_key},
                Key=today_backup_key
            )
            print(f"Daily backup created: {today_backup_key}")

            # Create weekly backup on Sundays
            if day_of_week == 6:  # Sunday
                weekly_backup_key = f"{WEEKLY_BACKUP_PREFIX}{today}/{file_name}"
                s3_client.copy_object(
                    Bucket=S3_BUCKET_NAME,
                    CopySource={'Bucket': S3_BUCKET_NAME, 'Key': file_key},
                    Key=weekly_backup_key
                )
                print(f"Weekly backup created: {weekly_backup_key}")

            # Create monthly backup on the first day of the month
            if first_day_of_month:
                monthly_backup_key = f"{MONTHLY_BACKUP_PREFIX}{today}/{file_name}"
                s3_client.copy_object(
                    Bucket=S3_BUCKET_NAME,
                    CopySource={'Bucket': S3_BUCKET_NAME, 'Key': file_key},
                    Key=monthly_backup_key
                )
                print(f"Monthly backup created: {monthly_backup_key}")

        return {"statusCode": 200, "body": "Backup process completed successfully"}
    except Exception as e:
        print(f"Error occurred during backup: {e}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
