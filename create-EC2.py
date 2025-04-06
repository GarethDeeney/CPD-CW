# Creates an EC2 instance
import boto3

client = boto3.client("ec2")
response = client.run_instances(
    ImageId="ami-08b5b3a93ed654d19",
    InstanceType="t2.micro",
    MaxCount=1,
    MinCount=1,
    KeyName="vockey",
    SecurityGroups=["launch-wizard-1"],
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": "CWEC2InstanceS0905538"}],
        }
    ],
)
print(response)
