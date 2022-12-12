from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import utils
from aws_lambda_powertools.utilities.typing import LambdaContext
import os
import boto3
import json

  

tracer = Tracer()
logger = Logger()
utils.copy_config_to_registered_loggers(source_logger=logger)

sqs_client = boto3.client("sqs")

@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info("Received message from SQS")
    queue_url = os.environ["SQS_URL"]
    print("queue_url is "+queue_url)
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    
    
    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")
        delete_message= sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
        print('delete_message', delete_message)

    
    return response