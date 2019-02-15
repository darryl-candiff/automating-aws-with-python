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
