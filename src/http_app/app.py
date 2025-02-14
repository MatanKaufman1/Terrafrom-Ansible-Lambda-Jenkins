import time
from flask import Flask, request, jsonify, render_template, Response
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import boto3
import json
#from lambda_handler.create_user.lambda_function import s3_client

app = Flask(__name__)
def get_client():
    return boto3.client(
        's3',
        region_name='eu-central-1'
    )
S3_BUCKET_NAME = 'bucket-matan'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/projects', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        project_name = data.get('project_name')
        suffix = data.get('suffix')

        if not project_name or not suffix:
            return jsonify({'error': 'Project name and suffix are required'}), 400
        lambda_payload = {
            'project_name': project_name,
            'suffix': suffix
        }
        lambda_client = boto3.client('lambda', region_name='eu-central-1')
        response = lambda_client.invoke(
            FunctionName='create_project',  # Replace with your Lambda function name
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=json.dumps(lambda_payload)
        )
        response_payload = json.loads(response['Payload'].read())
        if response.get('FunctionError'):
            return jsonify({'error': response_payload.get('errorMessage', 'Lambda function error')}), 500

        return jsonify({'status': 'success', 'message': response_payload.get('message')}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    s3_client = get_client()
    create_user_prefix= 'create_user/'
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return jsonify({'error': 'Username, email and password are required'}), 400
        user_data = {
            'user_name' : username,
            'email' : email,
            'password' : password
        }
        file_name = f"{create_user_prefix}{email}.json"

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(user_data),
            ContentType='application/json'
        )
        print(f"Uploading to bucket: {S3_BUCKET_NAME}, key: {file_name}")
        return jsonify({
            'status': 'success',
            'message': f'User {username} created successfully and saved to S3'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/backup', methods=['POST'])
def backup_file():
    BACKUP_PREFIX = 'backup_files/'
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Generate S3 key with the prefix
        filename = secure_filename(file.filename)
        s3_key = f"{BACKUP_PREFIX}{filename}"

        s3_client = get_client()
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, s3_key)

        return jsonify({
            'status': 'success',
            'message': f'File uploaded and backed up to S3 under {s3_key}'
        }), 200
    except Exception as e:
        print(f"Error in backup_file: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/whatsapp/send', methods=['POST'])
def send_whatsapp():
    try:
        data = request.get_json()
        phone = data.get('phone')
        message = data.get('message')

        if not phone or not message:
            return jsonify({'error': 'Phone and message are required'}), 400

        lambda_client = boto3.client('lambda', region_name='eu-central-1')
        payload = {
            "phone": phone,
            "message": message
        }
        # Invoke the Lambda function
        lambda_function_name = "send_whatsapp"
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',  # Use 'Event' for async invocation if needed
            Payload=json.dumps(payload)
        )

        # Read the response from the Lambda function
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))

        # Return the Lambda function's response to the frontend
        return jsonify(response_payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/convert/csv-to-excel', methods=['POST'])
def convert_csv_to_excel():
    CSV_PREFIX = 'csv_files/'
    EXCEL_PREFIX = 'excel_files/'
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400

        s3 = get_client()
        filename = secure_filename(file.filename)
        s3_key = f"{CSV_PREFIX}{filename}"
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=file)

        #  Fetch the latest file from "excel_file/" prefix
        time.sleep(5)
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=EXCEL_PREFIX)

        if 'Contents' not in response:
            return jsonify({'error': 'No files found in the specified prefix'}), 404

        files = response['Contents']
        latest_file = max(files, key=lambda x: x['LastModified'])
        latest_file_key = latest_file['Key']
        latest_file_content = s3.get_object(Bucket=S3_BUCKET_NAME, Key=latest_file_key)['Body'].read()

        # Return the latest file as a downloadable response
        response = Response(latest_file_content, mimetype='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename={latest_file_key.split("/")[-1]}'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/info/<resource_id>', methods=['GET'])
def get_info(resource_id):
    """
    Uploads the search subject to S3 to trigger the Lambda function,
    retrieves the processed file from S3, and sends it back to the user.
    """
    s3_client = boto3.client('s3')
    bucket_name = "bucket-matan"
    upload_prefix = "wikipedia_files/"
    processed_file_key = "wikipedia_file.txt"
    file_name = f"{resource_id.replace(' ', '_')}.txt"
    upload_key = f"{upload_prefix}{file_name}"
    try:
        local_file_path = f"/tmp/{file_name}"
        with open(local_file_path, "w") as file:
            file.write(resource_id)
        s3_client.upload_file(local_file_path, bucket_name, upload_key)
        os.remove(local_file_path)
        print(f"File uploaded to S3: {upload_key}")

        # Step 2: Poll for the processed file
        print(f"Waiting for processed file: {processed_file_key}")
        time.sleep(5)
        for _ in range(10):  # Poll up to 10 times, adjust as needed
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=processed_file_key)
            if "Contents" in response:
                print(f"Processed file found: {processed_file_key}")
                break
            time.sleep(5)  # Wait 5 seconds before retrying
        else:
            return jsonify({"error": "Processed file not available after timeout."}), 504

        local_processed_path = f"/tmp/{processed_file_key}"
        s3_client.download_file(bucket_name, processed_file_key, local_processed_path)
        print(f"Processed file downloaded: {local_processed_path}")

        with open(local_processed_path, "rb") as file:
            file_content = file.read()
        os.remove(local_processed_path)

        return Response(
            file_content,
            mimetype="text/plain",
            headers={"Content-Disposition": "attachment; filename=wikipedia_file.txt"}
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    # test 2


@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)