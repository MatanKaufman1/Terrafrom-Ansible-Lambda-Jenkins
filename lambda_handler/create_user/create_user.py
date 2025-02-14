from urllib.parse import unquote
import os
import json
import boto3
import requests

GITLAB_API_BASE_URL =  "http://3.126.51.24:80/api/v4"
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITLAB_TOKEN}"
}
s3_client = boto3.client('s3')

def create_gitlab_user( username, email, password):
    data = {
        "name": username,
        "username": username,
        "email": email,
        "password": password,
        "skip_confirmation": True
    }
    print(f"Creating GitLab user with data: {data}")
    try:
        response = requests.post(f"{GITLAB_API_BASE_URL}/users", headers=HEADERS, json=data)
        print(f"GitLab API response: {response.status_code}, {response.json()}")
        if response.status_code == 201:
            user_id = response.json()["id"]
            print(f"GitLab user created: {username} (ID: {user_id})")
            return user_id
        else:
            print(f"Failed to create GitLab user: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Error creating GitLab user: {e}")
    return None

def create_gitlab_group(group_name):
    group_path = f"{group_name.lower().replace(' ', '_')}_group"
    data = {
        "name": group_name,
        "path": group_path
    }
    print(f"Creating GitLab group with data: {data}")
    try:
        response = requests.post(f"{GITLAB_API_BASE_URL}/groups", headers=HEADERS, json=data)
        if response.status_code == 201:
            group_id = response.json()["id"]
            print(f"GitLab group created: {group_name} (ID: {group_id})")
            return group_id
        else:
            print(f"Failed to create GitLab group: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Error creating GitLab group: {e}")
    return None

def add_user_to_group(user_id, group_id):
    data = {
        "user_id": user_id,
        "access_level": 20  # "Reporter" role
    }
    print(f"Adding user {user_id} to group {group_id} with data: {data}")
    try:
        response = requests.post(f"{GITLAB_API_BASE_URL}/groups/{group_id}/members", headers=HEADERS, json=data)
        if response.status_code == 201:
            print(f"User {user_id} added to group {group_id} with Reporter role.")
        else:
            print(f"Failed to add user {user_id} to group {group_id}: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Error adding user {user_id} to group {group_id}: {e}")

def lambda_handler(event, context):
    print(f"Received S3 event: {json.dumps(event, indent=2)}")

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = unquote(record['s3']['object']['key'])
        print(f"Processing S3 object: Bucket={bucket_name}, Key={object_key}")

        if object_key.startswith('create_user/'):
            try:
                response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                user_data = json.loads(response['Body'].read().decode('utf-8'))
                print(f"Successfully retrieved and decoded data for {object_key}")
            except Exception as e:
                print(f"Error retrieving or decoding object {object_key}: {e}")
                continue
            username = user_data.get("user_name")
            email = user_data.get("email")
            password = user_data.get("password")
            print(f"Parsed user data: Username={username}, Email={email}, Password={password}")
            if not all([username, email, password]):
                print(f"Missing user data in {object_key}. Skipping.")
                continue
            user_id = create_gitlab_user(username=username, email=email, password=password)
            if user_id:
                print(f"User created successfully in GitLab: {username} (ID: {user_id})")

                group_id = create_gitlab_group(username)
                if group_id:
                    add_user_to_group(user_id, group_id)
                else:
                    print(f"Failed to create group for {username}")

def create_user_repository(username):
    data = {
        "name": username,
        "visibility": "private"
    }
    response = requests.post(f"{GITLAB_API_BASE_URL}/projects", headers=HEADERS, json=data)
    if response.status_code == 201:
        repo_url = response.json()["http_url_to_repo"]
        print(f"Repository created for {username}: {repo_url}")
    else:
        print(f"Failed to create repository for {username}: {response.status_code}, {response.json()}")
    # sharon and matan