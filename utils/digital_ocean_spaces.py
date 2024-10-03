import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

load_dotenv()

class DigitalOceanSpaces:
    def __init__(self):
        print("Connecting to DigitalOcean Spaces...")
        print(f"Region: {os.getenv('DO_SPACE_REGION')}")
        self.s3_client = boto3.client(
            's3',
            region_name=os.getenv("DO_SPACE_REGION"),
            endpoint_url=os.getenv("DO_SPACE_ENDPOINT"),
            aws_access_key_id=os.getenv("DO_SPACE_KEY"),
            aws_secret_access_key=os.getenv("DO_SPACE_SECRET")
        )
        self.bucket_name = os.getenv("DO_SPACE_NAME")

    def upload_file(self, file_path, object_name):
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return f"{os.getenv('DO_SPACE_ENDPOINT')}/{self.bucket_name}/{object_name}"
        except FileNotFoundError:
            return "File not found"
        except NoCredentialsError:
            return "Credentials not available"
        except ClientError as e:
            return str(e)

    def delete_file(self, object_name):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            return f"{object_name} deleted"
        except ClientError as e:
            return str(e)

    def get_file_url(self, object_name):
        return f"{os.getenv('DO_SPACE_ENDPOINT')}/{self.bucket_name}/{object_name}"

    def list_files(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            return [item['Key'] for item in response.get('Contents', [])]
        except ClientError as e:
            return str(e)
