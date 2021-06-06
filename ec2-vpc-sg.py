import boto3

ec2_client=boto3.resource('ec2', region_name='us-east-1')

#Create Vpc
vpc=ec2_client.create_vpc(CidrBlock='10.0.0.0/16')
vpc.create_tags(Tags=[{"Key": "Name", "Value": "new_vpc"}])
vpc.wait_until_available()
print(vpc.id)

# create & attach IG
ig=ec2_client.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

#create a public route
route_table=vpc.create_route_table()
route=route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id
)
print(route_table.id)

#create subnet
subnet=ec2_client.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc.id)
print(subnet.id)

#associate the route table with subnet
route_table.associate_with_subnet(SubnetId=subnet.id)

#create sec grp
sec_group=ec2_client.create_security_group(
    GroupName='subnet1', Description='new subnet', VpcId=vpc.id
)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22
)
print(sec_group.id)

#Create Instance
instances=ec2_client.create_instances(
    ImageId='ami-0d5eff06f840b45e9',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='latestNV',
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}]
)
instances[0].wait_until_running()
print(instances[0].id)