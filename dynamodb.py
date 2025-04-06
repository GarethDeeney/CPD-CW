# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import boto3

# Get the service resource.
dynamodb = boto3.resource("dynamodb")

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName="ImageComparisonS0905538",
    KeySchema=[{"AttributeName": "ImageName", "KeyType": "HASH"}],
    AttributeDefinitions=[{"AttributeName": "ImageName", "AttributeType": "S"}],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

# Wait until the table exists.
table.meta.client.get_waiter("table_exists").wait(TableName="ImageComparisonS0905538")

# add dummy image item to check table creates correctly
table.put_item(
    Item={
        "ImageName": "Dummy Image",
        "Similarity": "0.00",
        "ForegroundBrightness": "100",
        "BackgroundBrightness": "100",
    }
)

# Print out some data about the table.
print(table.item_count)
