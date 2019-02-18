import os
import urllib
import boto3

def start_label_detection(bucketname, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucketname,
                'Name': key
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
        })
    print("Bucket name:",bucketname)
    print("Key:", key)
    print(rekognition_client)
    print( os.environ['REKOGNITION_SNS_TOPIC_ARN'])
    print(os.environ['REKOGNITION_ROLE_ARN'])
    print(response.keys())
    print(response['JobId'])
    print(response['ResponseMetadata'])

    return

def start_processing_video(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        start_label_detection(bucket_name, urllib.parse.unquote_plus(key))

    return

def handle_label_detection(event, context):

    print(event)

    return
