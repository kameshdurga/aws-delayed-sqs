from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import utils
from aws_lambda_powertools.utilities.typing import LambdaContext
import emoji
import os
import boto3
from botocore.exceptions import ClientError

tracer = Tracer()
logger = Logger()
utils.copy_config_to_registered_loggers(source_logger=logger)

def create_data(message, subject):
    table_name = os.environ["table_name"]
    table = boto3.resource('dynamodb').Table(table_name)
    # client.publish(
    #     TopicArn=topic_arn, Message=message, Subject=subject)

    try:
        table.put_item(
                Item={
                    'OrderID': 1,
                    'CustomerID': 123,
                    'product': "Harry potter book",
                    'quantity': 2,
                    'status': "NEW"})
        table.put_item(
                Item={
                    'OrderID': 2,
                    'CustomerID': 123,
                    'product': "shoe",
                    'quantity': 1,
                    'status': "NEW"})
    except ClientError as err:
        logger.error("couldnt update the table")
        raise


@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(emoji.emojize("Python is :thumbs_up:"))
    message = "Hello from lambda!"
    subject = "From  Lambda"
    create_data(message, subject)
    return {"statusCode": 200, "body": "Hello, world!"}
