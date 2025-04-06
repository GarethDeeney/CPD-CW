import boto3
import json

def lambda_handler(event, context):
    # Get event body
    body = json.loads(event['Records'][0]['body'])
    record = body['Records'][0]

    # Get bucket and image name to pass to rekognition for comparions
    bucketName = record['s3']['bucket']['name']
    imageName = record['s3']['object']['key']

    print(f'Bucket Name: {bucketName}')
    print(f'Image Name: {imageName}')

    # run amazon rekognition and return similarity, foreground and background brightness
    similarity,foregroundBrightness, backgroundBrightness = runRekognition(bucketName, imageName)

    # update dynamo db with scores 
    updateDynamoDB(imageName, similarity, foregroundBrightness, backgroundBrightness)

    # check similarity and background brightness and send email if within range
    if similarity < 1 and backgroundBrightness < 10:
        publishMessage("No face match was found and the background brightness of the image was less than 10.") 

def publishMessage(message):
    client = boto3.client('sns')
    response = client.publish(TopicArn='arn:aws:sns:us-east-1:533267268565:cwtopicS0905538', Message=message)
    print("Message published")
    
def updateDynamoDB(imageName, similarity, foregroundBrightness, backgroundBrightness):
   # rekognition response to store in dynamodb table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ImageComparisonS0905538') 

    # add results to database
    dynamo = table.put_item(
        Item={
            'ImageName': imageName,
            'Similarity': str(similarity),
            'ForegroundBrightness': str(foregroundBrightness),
            'BackgroundBrightness': str(backgroundBrightness)
        }
    )

    print("DynamoDB updated")
    
def runRekognition(bucketName, imageName):
    # get similarity score from compareFaces method
    similarity = compareFaces(bucketName, imageName)

    # get brightness scores from detectLabels method and print results
    foregroundBrightness, backgroundBrightness = detectLabels(bucketName, imageName)
    # foregroundBrightness, backgroundBrightness = labels
    
    print(f'Similarity: {similarity}')
    print(f'Foreground Brightness: {foregroundBrightness}')
    print(f'Background Brightness: {backgroundBrightness}')
    
    return similarity, foregroundBrightness, backgroundBrightness

def compareFaces(bucketName, imageName):
    rekognition = boto3.client('rekognition', region_name='us-east-1')

    # compare faces with group.png photo with image using rekognition 
    response = rekognition.compare_faces(
        SimilarityThreshold=80,
        SourceImage={ 'S3Object': {'Bucket': bucketName, 'Name': 'groupphoto.png'}},
        TargetImage={'S3Object': {'Bucket': bucketName, 'Name': imageName}} 
    )
    # check for a face match and return 0 if none found
    if(len(response['FaceMatches']) == 0):
        return 0

    # else set and return similarity score 
    similarity = response['FaceMatches'][0]['Similarity']
    return similarity

def detectLabels(bucketName, imageName):
    rekognition = boto3.client('rekognition', region_name='us-east-1')

    # get image property results from detect_labels method
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': imageName
            }
        },
        MaxLabels=10,
        MinConfidence=90,
        Features= [ "GENERAL_LABELS", "IMAGE_PROPERTIES" ],
        Settings= { }
    )

    # set brightness results to variables to return
    foregroundBrightness = response["ImageProperties"]["Foreground"]["Quality"]["Brightness"]
    backgroundBrightness = response["ImageProperties"]["Background"]["Quality"]["Brightness"]

    # return brightness results 
    return foregroundBrightness, backgroundBrightness
