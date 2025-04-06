import boto3
import time

client = boto3.client('s3')

print('Uploading Image 2...')
client.upload_file('./image2.jpg', 'courseworkstack-s0905538-myawsbucket-533267268565', 'image2' )

print('Waiting 30 seconds ...')
time.sleep(30)
print('Waited 30 seconds ...')

print('Uploading Image 4...')
client.upload_file('./image4.jpg','courseworkstack-s0905538-myawsbucket-533267268565', 'image4')
print('All files uploaded to S3 bucket')
