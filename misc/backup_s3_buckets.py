import boto3
from datetime import datetime, timedelta

def get_bucket_objects(bucket_name):
    """
    Get a list of objects in a bucket
    """
    s3 = boto3.client('s3')
    objects = []

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            objects = response['Contents']
    except Exception as e:
        print(f"Error occurred while listing objects in {bucket_name}: {str(e)}")

    return objects

def turn_off_versioning(bucket_name):
    """
    Turn off versioning for the bucket if it's enabled
    """
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_versioning(Bucket=bucket_name)
        if 'Status' in response and response['Status'] == 'Enabled':
            s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={
                    'Status': 'Suspended'
                }
            )
            print(f"Versioning turned off for bucket: {bucket_name}")
        else:
            print(f"Versioning is not enabled for bucket: {bucket_name}")
    except Exception as e:
        print(f"Error occurred while checking or turning off versioning for bucket {bucket_name}: {str(e)}")
        
def move_objects_to_backup(bucket_name, objects):
    """
    Move objects to backup bucket
    """
    s3 = boto3.client('s3')
    backup_bucket_name = f"{bucket_name}-backup"

    # Check if backup bucket exists, create if it doesn't
    try:
        s3.head_bucket(Bucket=backup_bucket_name)
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            s3.create_bucket(Bucket=backup_bucket_name)
            print(f"Created backup bucket: {backup_bucket_name}")
        else:
            print(f"Error occurred while checking backup bucket: {str(e)}")
            return

    # Move objects to backup bucket
    for obj in objects:
        try:
            copy_source = {'Bucket': bucket_name, 'Key': obj['Key']}
            s3.copy_object(CopySource=copy_source, Bucket=backup_bucket_name, Key=obj['Key'])
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Moved object {obj['Key']} from {bucket_name} to {backup_bucket_name}")
        except Exception as e:
            print(f"Error occurred while moving object {obj['Key']}: {str(e)}")

    # Check if source bucket is empty after migration
    if not get_bucket_objects(bucket_name):
        try:
            s3.delete_bucket(Bucket=bucket_name)
            print(f"Deleted empty bucket: {bucket_name}")
        except Exception as e:
            print(f"Error occurred while deleting bucket {bucket_name}: {str(e)}")
    else:
        print(f"Source bucket {bucket_name} is not empty after migration. Please empty it before deletion.")

def delete_old_objects(bucket_name, objects, days):
    """
    Delete objects older than a certain number of days
    """
    s3 = boto3.client('s3')

    cutoff_date = datetime.now() - timedelta(days=days)
    for obj in objects:
        last_modified = obj['LastModified'].replace(tzinfo=None)
        if last_modified < cutoff_date:
            try:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted object {obj['Key']} from {bucket_name}")
            except Exception as e:
                print(f"Error occurred while deleting object {obj['Key']}: {str(e)}")

def main():
    # Read bucket names from a file
    with open('bucket_names.txt', 'r') as f:
        bucket_names = [line.strip() for line in f if line.strip()]

    for bucket_name in bucket_names:
        print(f"Processing bucket: {bucket_name}")
        objects = get_bucket_objects(bucket_name)
        if objects:
            move_objects_to_backup(bucket_name, objects)
            delete_old_objects(bucket_name, objects, 30)
            turn_off_versioning(bucket_name)
        else:
            print(f"No objects found in {bucket_name}. No action needed.")

if __name__ == "__main__":
    main()
