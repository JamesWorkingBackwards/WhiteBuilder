# AIClassifier.py: A Lambda function to react to new objects placed in S3,
# run them through AWS Rekognition, and store the results in a database (Dyanamo)
# to provide instant intelligence for customers on their data
# during a WhiteBuilding session
# TODO: Extent to other AI services
# TODO: Write to Parquet in S3 for SQL support using Athena

from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')

rekognition = boto3.client('rekognition',region_name='us-east-1')


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key):
    print (bucket);
    print (key);
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    # TODO: replace the table with something dynamically generated
    table = boto3.resource('dynamodb').Table('whitebuild-jan152018')
    labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    
    labelString = ""
    
    for label in labels:  # this gets you a list of IPs
      labelString += label['Name'] + ";"
      
    table.put_item(Item={'PK': key, 'type': 'Labels', 'value': labelString})
    
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response


def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    # Calls rekognition DetectFaces API to detect faces in S3 object
    #response = detect_faces(bucket, key)

    # Calls rekognition DetectLabels API to detect labels in S3 object
    response = detect_labels(bucket, key)

    # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
    #response = index_faces(bucket, key)

    # Print response to console.
    print(response)

    return response
