import boto3
from datetime import datetime, timezone, timedelta
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize a Boto3 S3 client
s3 = boto3.client('s3')

# Define the bucket name and age limit in minutes
bucket_name = 'manish-data'
age_limit_minutes = 3  # Example: 30 minutes
age_limit = datetime.now(timezone.utc) - timedelta(minutes=age_limit_minutes)

def lambda_handler(event, context):
    try:
        # List objects in the specified bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' not in response:
            logger.info('No objects found in the bucket.')
            return {
                'statusCode': 200,
                'body': 'No objects found in the bucket.'
            }

        # Iterate over the list of objects
        for obj in response['Contents']:
            object_key = obj['Key']
            object_last_modified = obj['LastModified']

            # Check if the object is older than the age limit
            if object_last_modified < age_limit:
                # Delete the object
                s3.delete_object(Bucket=bucket_name, Key=object_key)
                logger.info(f'Deleted object: {object_key}')

        return {
            'statusCode': 200,
            'body': 'Operation completed successfully.'
        }

    except Exception as e:
        logger.error(f'Error processing bucket {bucket_name}: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Error processing bucket {bucket_name}: {str(e)}'
        }
