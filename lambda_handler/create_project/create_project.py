import os
import json
import requests

GITLAB_API_BASE_URL = "https://gitlab.com/api/v4"
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_USERNAME = 'MY_USER_NAME'


def lambda_handler(event, context):
    try:
        project_name = event.get('project_name')
        suffix = event.get('suffix')
        if not project_name or not suffix:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Project name and suffix are required'})
            }

        allowed_suffixes = ['c', 'py', 'yaml']
        if suffix not in allowed_suffixes:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': f'Invalid suffix. Allowed values are: {", ".join(allowed_suffixes)}'})
            }

        project = create_gitlab_project(project_name)
        project_id = project['id']
        print(f"Created GitLab project: {project_name} with ID: {project_id}")


        file_name = f"main.{suffix}"
        file_content = ""  # Empty file
        upload_file_to_gitlab(project_id, file_name, file_content)
        print(f"Uploaded file: {file_name} to project: {project_name}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Project {project_name} created and file {file_name} uploaded to GitLab.'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }


def create_gitlab_project(project_name):
    """
    Create a new project in GitLab.
    """
    gitlab_api_url = f"{GITLAB_API_BASE_URL}/projects"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {"name": project_name}
    response = requests.post(gitlab_api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def upload_file_to_gitlab(project_id, file_path, file_content):
    """
    Upload a file to a GitLab repository.
    """
    gitlab_api_url = f"{GITLAB_API_BASE_URL}/projects/{project_id}/repository/files/{file_path}"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {
        "branch": "master",
        "content": file_content,
        "commit_message": f"Add {file_path}"
    }
    response = requests.post(gitlab_api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
