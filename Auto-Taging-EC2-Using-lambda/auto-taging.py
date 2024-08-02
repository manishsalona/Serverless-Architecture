import boto3
import datetime
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    try:
        # Log the entire event to understand its structure
        logger.info(f"Received event: {event}")
        
        # Ensure 'instance-id' key exists in the event
        instance_id = event.get('instance-id')
        if not instance_id:
            raise KeyError("'instance-id' key not found in the event")
        
        # Get the current date in YYYY-MM-DD format
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Retrieve custom tags from the event or initialize as an empty list if not present
        custom_tags = event.get('tags', [])
        
        # Add the current date tag
        custom_tags.append({'Key': 'LaunchDate', 'Value': current_date})
        
        # Apply the tags to the specified instance
        ec2.create_tags(Resources=instance_id, Tags=custom_tags)
        
        # Log the success message
        logger.info(f"Successfully tagged instance {instance_id} with tags {custom_tags}")
        
        # Return a successful response
        return {
            'statusCode': 200,
            'body': f"Successfully tagged instance {instance_id} with tags {custom_tags}"
        }
    
    except KeyError as e:
        # Log the KeyError and return a response with a 400 status code
        logger.error(f"KeyError: {str(e)} - Check if the event structure matches the expected format.")
        return {
            'statusCode': 400,
            'body': f"KeyError: {str(e)} - Check if the event structure matches the expected format."
        }
    
    except Exception as e:
        # Log any other errors and return a response with a 500 status code
        logger.error(f"Error tagging instance: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error tagging instance: {str(e)}"
        }
