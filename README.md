# Flask Web App with AWS Lambda Integration

## Overview:

This project is a Flask-based web application that interacts with various AWS Lambda functions. It allows users to perform several operations including creating projects, managing users, sending WhatsApp messages, converting CSV files to Excel, and performing backups. The application communicates with Lambda functions deployed on AWS to handle backend tasks.
Project Structure

## Structure:

    ├── Dockerfile
    ├── infrastructure
    │   ├── ansible
    │   └── terraform
    ├── Jenkinsfile
    ├── lambda_handler
    │   ├── backup
    │   ├── create_project
    │   ├── create_user
    │   ├── csv_to_excel
    │   ├── get_info
    │   ├── send_whatsapp
    │   └── tests
    ├── README.md
    └── src
        └── http_app
            ├── app.py
            ├── requirements.txt
            └── templates
                └── index.html

## Key Components:

Dockerfile: Defines the image build process for the Flask app.
lambda_handler: Contains the individual Python Lambda handlers (e.g., create project, backup, CSV to Excel conversion, etc.).
infrastructure: Holds Ansible and Terraform configurations for provisioning infrastructure.
src/http_app: Contains the Flask app with routes that trigger AWS Lambda functions.
Jenkinsfile: Defines the pipeline for continuous integration and deployment.

## Features:

Create Projects: Calls a Lambda function to create a new project.
Create Users: Stores user data in AWS S3 and triggers Lambda for further processing.
Backup Files: Uploads files to AWS S3 for backup.
Send WhatsApp Messages: Invokes a Lambda function to send messages using the WhatsApp API.
CSV to Excel Conversion: Converts CSV files uploaded to S3 into Excel files.
Health Check Endpoint: Exposes an endpoint (/health) for monitoring the status of the application.

## Prerequisites:

AWS Account: Ensure you have an AWS account and IAM permissions to manage Lambda, S3, and other required services.
Docker: To run the app in a containerized environment.
Terraform: To provision and manage infrastructure.
Ansible: Used to configure and manage servers like Jenkins and GitLab.
Jenkins: For CI/CD pipeline automation.

## Setup and Installation:

Clone this repository:

    git clone https://github.com/MatanKaufman1/Terrafrom-Ansible-Lambda-Jenkins.git

Build the Docker image:

    docker build -t flask-lambda-webapp .

Run the Docker container:

    docker run -p 5000:5000 flask-lambda-webapp

    The application will be available at http://localhost:5000.

Lambda Functions:

This web app interacts with the following AWS Lambda functions:

    Create Project: Creates a new project with the given name and suffix.
    Create User: Creates a new user and stores the data in an S3 bucket.
    Send WhatsApp: Sends a WhatsApp message using an external service.
    CSV to Excel: Converts CSV files uploaded to S3 into Excel format.
    Backup: Backs up files uploaded through the API to S3.

Each of these Lambda functions is invoked through the web app’s RESTful API endpoints.
API Endpoints

    POST /api/projects: Creates a new project by invoking the create_project Lambda function.
    POST /api/users: Creates a new user and uploads the data to S3.
    POST /api/backup: Uploads a file to S3 for backup.
    POST /api/whatsapp/send: Sends a WhatsApp message using the send_whatsapp Lambda function.
    POST /api/convert/csv-to-excel: Converts a CSV file to Excel format and returns it.
    GET /api/info/<resource_id>: Retrieves processed information related to a resource.
    /health: Health check endpoint for the application.

Deployment

To deploy the application and Lambda functions, use Terraform and Ansible. The Terraform configuration in infrastructure/terraform provisions the required AWS resources, and Ansible handles the server configuration for Jenkins and GitLab.
Example Terraform Command:

terraform init
terraform apply

Testing

Unit tests for Lambda functions are available in the lambda_handler/tests directory. You can use pytest to run the tests.
