from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import utils
from aws_lambda_powertools.utilities.typing import LambdaContext
import emoji
import os
import boto3

  

tracer = Tracer()
logger = Logger()
utils.copy_config_to_registered_loggers(source_logger=logger)


@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(emoji.emojize("Python is :thumbs_up:"))
    for record in event['Records']:
        print("test")
        payload = record["body"]
        print(str(payload))
    return {"statusCode": 200, "body": "Hello, world!"}
