import boto3
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Describe instances with Auto-Stop tag
    stop_response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Auto-Stop', 'Values': ['true']}
        ]
    )

    # Describe instances with Auto-Start tag
    start_response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Auto-Start', 'Values': ['true']}
        ]
    )

    # List to hold instance IDs
    stop_instances = []
    start_instances = []

    # Extract instance IDs to stop
    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])

    # Extract instance IDs to start
    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    # Stop instances
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        logger.info(f'Stopped instances: {stop_instances}')
    else:
        logger.info('No instances to stop.')

    # Start instances
    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        logger.info(f'Started instances: {start_instances}')
    else:
        logger.info('No instances to start.')

    return {
        'statusCode': 200,
        'body': 'Operation completed successfully.'
    }
