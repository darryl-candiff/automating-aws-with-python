key_name = 'python_automation_key'
img = ec2.Image('ami-0fad7378adf284ce0')
img.name
ami_name = 'amzn2-ami-hvm-2.0.20190115-x86_64-gp2'
filters = [{'Name': 'name', 'Values': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances[0]
instances[0].terminate()
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)

sg = ec2. SecurityGroup(inst_sg[0]['GroupId])
sg = ec2. SecurityGroup(inst_sg[0]['GroupId'])
sg
sg.ip_permissions
response = sg.authorize_ingress(
'FromPort': 80,
'IpProtocol': 'tcp',
'CidrIp': '8.8.8.8/32',
'ToPort': 80,
'UserIdGroupPairs': [])
response = sg.authorize_ingress(IpPermissions=[{
'FromPort': 80,
'IpProtocol': 'tcp',
'IpRanges': [{'CidrIp': '8.8.8.8/32'}],
'ToPort': 80,
}])
inst_sg = inst.security_groups
inst_sg

paginator = as_client.get_paginator()
paginator = as_client.describe_auto_scaling_groups()
paginator
paginator[0]['AutoScalingGroupName']
paginator['AutoScalingGroups'][0]['AutoScalingGroupName']
as_client.execute_policy(AutoScalingGroupName=paginator['AutoScalingGroups'][0]['AutoScalingGroupName'], Policyname='Scale Up')
as_client.execute_policy(AutoScalingGroupName=paginator['AutoScalingGroups'][0]['AutoScalingGroupName'], Policyname='Scale Up')
paginator['AutoScalingGroups'][0]['AutoScalingGroupName']
group_name = paginator['AutoScalingGroups'][0]['AutoScalingGroupName']
as_client.execute_policy(AutoScalingGroupName=group_name, PolicyName='Scale Up', HonorCooldown=False)


import requests
data = {"text":"Hello, World!"}
url = 'https://hooks.slack.com/services/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'
requests.post(url, json=data)
