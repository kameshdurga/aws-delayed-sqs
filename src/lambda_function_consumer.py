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
        orderDetails = json.loads(message_body)
        print(f"Message body: {orderDetails}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")
        
        table_name = os.environ["table_name"]
        table = boto3.resource('dynamodb').Table(table_name)
        delete_message= sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
        print('delete_message', delete_message)
        
        item = table.get_item(Key={ 'OrderID': orderDetails['Keys']['OrderID']['N'], 'CustomerID':  orderDetails['Keys']['CustomerID']['N']})   
        print(item)
    
    return response