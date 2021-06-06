import boto3
s3_client=boto3.client('s3')
file_reader=open('main.py').read()
resp=s3_client.put_object(
    ACL='private',
    Body=file_reader,
    Bucket='newbucketmay20th2020',
    Key='main.py'
)