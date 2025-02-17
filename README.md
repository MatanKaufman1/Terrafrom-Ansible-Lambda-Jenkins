# Lambda-Powered Flask Web App

## Overview
This project is a Flask-based web application that interacts with multiple AWS Lambda functions and Amazon S3. It provides APIs for creating projects, user management, file backups, WhatsApp messaging, CSV-to-Excel conversion, and Wikipedia file processing.

## Features
- **Project Creation**: Calls a Lambda function to create projects.
- **User Management**: Stores user data in an S3 bucket.
- **File Backup**: Uploads files to an S3 bucket for backup.
- **WhatsApp Messaging**: Sends WhatsApp messages via a Lambda function.
- **CSV to Excel Conversion**: Uploads CSV files to S3 and retrieves processed Excel files.
- **Wikipedia File Processing**: Uploads and retrieves processed Wikipedia data via Lambda and S3.
- **Health Check**: Returns application status and timestamp.

## Technologies Used
- **Python** (Flask)
- **AWS Lambda**
- **Amazon S3**
- **Boto3** (AWS SDK for Python)

## Prerequisites
Ensure you have the following installed and configured:
- Python 3.x
- AWS CLI configured with credentials
- Required Python packages (install with `pip install -r requirements.txt`)

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up AWS credentials:
   ```sh
   aws configure
   ```
4. Run the Flask app:
   ```sh
   python app.py
   ```

## API Endpoints
### 1. Home Page
- **GET /**
- Returns the main page.

### 2. Create Project
- **POST /api/projects**
- **Request Body:**
  ```json
  {
    "project_name": "my_project",
    "suffix": "v1"
  }
  ```
- Calls the `create_project` Lambda function.

### 3. Create User
- **POST /api/users**
- **Request Body:**
  ```json
  {
    "username": "JohnDoe",
    "email": "john@example.com",
    "password": "securepassword"
  }
  ```
- Stores user data in S3 under `create_user/`.

### 4. Backup File
- **POST /api/backup**
- **Request:** Multipart form with `file`.
- Uploads file to S3 under `backup_files/`.

### 5. Send WhatsApp Message
- **POST /api/whatsapp/send**
- **Request Body:**
  ```json
  {
    "phone": "+1234567890",
    "message": "Hello from Lambda!"
  }
  ```
- Calls the `send_whatsapp` Lambda function.

### 6. Convert CSV to Excel
- **POST /api/convert/csv-to-excel**
- **Request:** Multipart form with a `.csv` file.
- Uploads CSV to S3, waits for an Excel file, and returns the processed file.

### 7. Get Wikipedia Processed Info
- **GET /api/info/<resource_id>**
- Uploads a text file with `resource_id` to S3, triggers Lambda, and retrieves the processed file.

### 8. Health Check
- **GET /health**
- Returns:
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-02-17T12:34:56.789Z"
  }
  ```

## Environment Variables
- `AWS_REGION=eu-central-1`
- `S3_BUCKET_NAME=bucket-matan`

## Deployment
For production deployment, consider using **Gunicorn** with **NGINX**:
```sh
pip install gunicorn
```
Run the app with:
```sh
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```



