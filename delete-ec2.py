import boto3
ec2_client=boto3.client('ec2', region_name='us-east-1')
instances=ec2_client.terminate_instances(
    InstanceIds=[
        'i-0a306bc34533f129d',
    ]
)