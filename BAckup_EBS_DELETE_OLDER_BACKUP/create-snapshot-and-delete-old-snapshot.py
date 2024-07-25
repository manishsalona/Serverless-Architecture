import boto3
from datetime import datetime, timezone, timedelta
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize a Boto3 EC2 client
ec2 = boto3.client('ec2')

def create_snapshot(volume_id, description):
    try:
        snapshot = ec2.create_snapshot(VolumeId=volume_id, Description=description)
        logger.info(f"Created snapshot: {snapshot['SnapshotId']} for volume: {volume_id}")
        return snapshot['SnapshotId']
    except Exception as e:
        logger.error(f"Error creating snapshot for volume {volume_id}: {e}")

def delete_old_snapshots(retention_minutes=1):
    try:
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        current_time = datetime.now(timezone.utc)
        retention_period = timedelta(minutes=retention_minutes)
        
        for snapshot in snapshots:
            snapshot_id = snapshot['SnapshotId']
            start_time = snapshot['StartTime']

            if current_time - start_time.replace(tzinfo=timezone.utc) > retention_period:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                logger.info(f"Deleted snapshot: {snapshot_id} as it was older than {retention_minutes} minutes")
    except Exception as e:
        logger.error(f"Error listing or deleting snapshots: {e}")

def lambda_handler(event, context):
    volume_id = 'vol-01f49f8cd88d79fbb'  # Replace with your EBS volume ID
    description = 'Snapshot created by Lambda function'

    # Create a snapshot for the specified EBS volume
    create_snapshot(volume_id, description)

    # List snapshots and delete those older than 30 minutes
    delete_old_snapshots()

    return {
        'statusCode': 200,
        'body': 'Operation completed successfully.'
    }
