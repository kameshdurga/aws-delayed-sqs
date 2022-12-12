from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import utils
from aws_lambda_powertools.utilities.typing import LambdaContext
import emoji
import os
import boto3
import json



def send_event(message, subject):
    client = boto3.client("sqs")
    queue_url = os.environ["SQS_URL"]
    # client.publish(
    #     TopicArn=topic_arn, Message=message, Subject=subject)
    response = client.send_message(
    QueueUrl=queue_url,
    DelaySeconds=600,
    MessageAttributes={
        'OrderDetails': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        }
    },
    MessageBody=message
)
    print("sent message succesfully")


tracer = Tracer()
logger = Logger()
utils.copy_config_to_registered_loggers(source_logger=logger)

print('Loading function')

@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(emoji.emojize("Python is :thumbs_up:"))
    message = "Hello from lambda!"
    subject = "From  Lambda"
    for record in event['Records']:
        print(record['eventID'])
        print(record['eventName'])
        print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
        send_event(json.dumps(record['dynamodb'], indent=2),"test")
    return 'Successfully processed {} records.'.format(len(event['Records']))
