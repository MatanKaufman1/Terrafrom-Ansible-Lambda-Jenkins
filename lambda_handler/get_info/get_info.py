import wikipediaapi
import boto3
import os

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = "BUCKET_NAME"
    wikipedia_file_key = "wikipedia_file.txt"
    prefix = "wikipedia_files/"

    try:
        print("Received event:", event)
        object_key = event['Records'][0]['s3']['object']['key']
        print(f"Processing S3 object: {object_key}")

        if not object_key.startswith(prefix):
            print(f"Object {object_key} is not in the '{prefix}' prefix. Skipping.")
            return {
                'statusCode': 400,
                'body': f"Error: File '{object_key}' is not in the '{prefix}' prefix."
            }

        local_file_path = f"/tmp/{os.path.basename(object_key)}"
        s3_client.download_file(bucket_name, object_key, local_file_path)
        print(f"Downloaded file from S3: {object_key} to {local_file_path}")

        with open(local_file_path, "r") as file:
            subject = file.read().strip()
        print(f"Extracted subject: {subject}")

        if not subject:
            print("Error: Subject is empty or missing.")
            return {
                'statusCode': 400,
                'body': "Error: Subject is missing from the input file."
            }

        wiki_wiki = wikipediaapi.Wikipedia('wiki-proj', 'en')
        page = wiki_wiki.page(subject)
        top_of_page = page.summary

        if page.exists():
            print(f"Found Wikipedia page for subject: {subject}")


            try:
                local_wikipedia_file = f"/tmp/{wikipedia_file_key}"
                s3_client.download_file(bucket_name, wikipedia_file_key, local_wikipedia_file)
                print(f"Downloaded existing wikipedia_file.txt.")
            except s3_client.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print(f"wikipedia_file.txt does not exist. Creating a new one.")
                    with open(local_wikipedia_file, "w", encoding="utf-8") as file:
                        file.write("")
                else:
                    raise


            with open(local_wikipedia_file, "a", encoding="utf-8") as file:
                file.write(f"Summary for {subject}:\n{top_of_page}\n\n")
            print("Appended summary to local wikipedia_file.txt.")


            s3_client.upload_file(local_wikipedia_file, bucket_name, wikipedia_file_key)
            print("Uploaded updated wikipedia_file.txt to S3.")

            os.remove(local_file_path)
            os.remove(local_wikipedia_file)
            print("Temporary files cleaned up.")
            return {
                'statusCode': 200,
                'body': f"Successfully appended summary of '{subject}' to {wikipedia_file_key}."
            }
        else:
            print(f"Error: The page '{subject}' does not exist on Wikipedia.")
            return {
                'statusCode': 404,
                'body': f"Error: The page '{subject}' does not exist on Wikipedia."
            }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }

