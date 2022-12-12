from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import utils
from aws_lambda_powertools.utilities.typing import LambdaContext
import os
import boto3

  

tracer = Tracer()
logger = Logger()
utils.copy_config_to_registered_loggers(source_logger=logger)

sqs_client = boto3.client("sqs")

@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info("Received message from SQS")
    queue_url = os.environ["SQS_URL"]
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=4,
        VisibilityTimeout=60 #14400
    )
    if('Messages' in response):
        logger.info("received response")
        logger.info("received message is " + response['Messages'])
        return response['Messages']
    else:
        print("No messages in queue.")
        return None
