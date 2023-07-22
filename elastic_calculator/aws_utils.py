import os

import boto3


def text_file_from_s3(bucket: str, key: str) -> str:
    """
    Helper function for reading text files from AWS S3 bucket.
    """
    session = boto3.Session(
        aws_access_key_id=os.getenv("ELASTIC_CALCULATOR_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("ELASTIC_CALCULATOR_AWS_SECRET_ACCESS_KEY"),
        aws_session_token=None,
    )
    s3_client = session.client("s3")
    content = s3_client.get_object(Bucket=bucket, Key=key)
    return content.get("Body").read().decode("utf-8")
