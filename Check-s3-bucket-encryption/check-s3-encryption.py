import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize a boto3 S3 client
    s3 = boto3.client('s3')
    log = []

    try:
        # List all S3 buckets
        response = s3.list_buckets()
        buckets = response['Buckets']

        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Check if bucket has encryption enabled
                encryption = s3.get_bucket_encryption(Bucket=bucket_name)
                rules = encryption['ServerSideEncryptionConfiguration']['Rules']
                log.append(f"Bucket {bucket_name} is encrypted with rules: {rules}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    log.append(f"Bucket {bucket_name} is not encrypted")
                else:
                    log.append(f"Error checking bucket {bucket_name}: {e}")

    except ClientError as e:
        log.append(f"Error listing buckets: {e}")

    # Log to CloudWatch
    print("\n".join(log))

    return {
        'statusCode': 200,
        'body': json.dumps(log)
    }

# For local testing, you can call the function directly
if __name__ == "__main__":
    event = {}
    context = {}
    lambda_handler(event, context)
