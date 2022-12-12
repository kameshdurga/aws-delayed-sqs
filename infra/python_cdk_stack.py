from aws_solutions_constructs.aws_eventbridge_lambda import EventbridgeToLambda

from aws_cdk.aws_lambda_event_sources import SqsEventSource

from aws_cdk.aws_lambda_event_sources import DynamoEventSource



from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda_python_alpha as python_,
    aws_lambda,
    aws_events as events,
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    Duration as duration
  
)
from constructs import Construct



class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_table = dynamodb.Table(
            self, "demo_table",
            partition_key=dynamodb.Attribute(
                name="OrderID",
                type=dynamodb.AttributeType.NUMBER
            ),sort_key=dynamodb.Attribute(
                name="CustomerID",
                type=dynamodb.AttributeType.NUMBER
            ),
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES
        )
   
        dynamo_db_policy =  iam.PolicyStatement(actions = ['dynamodb:*'],resources = [demo_table.table_arn])

        powertools_layer = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            id="lambda-powertools",
            layer_version_arn=f"arn:aws:lambda:{self.region}:017000801446:layer:AWSLambdaPowertoolsPython:39",
        )

        lambda_function = python_.PythonFunction(
            self,
            "AppStart",
            entry="src",
            handler="handler",
            index="lambda_function.py",
            layers=[powertools_layer],
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            environment = {'table_name': demo_table.table_name,},
        )

        lambda_function.add_to_role_policy(dynamo_db_policy)


        queue = sqs.Queue(self,"demo_delay_queue",delivery_delay=Duration.minutes(10))
        sqsPolicy =  iam.PolicyStatement(actions = ['sqs:*'],resources = [queue.queue_arn])

        lambda_function_producer = python_.PythonFunction(
            self,
            "AppProducer",
            entry="src",
            handler="handler",
            index="lambda_function_producer.py",
            layers=[powertools_layer],
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            environment = {'SQS_URL': queue.queue_url,},
        )

        lambda_function_producer.add_to_role_policy(sqsPolicy)
        lambda_function_producer.add_to_role_policy(dynamo_db_policy)

        lambda_function_producer.add_event_source(DynamoEventSource(demo_table,
    starting_position=aws_lambda.StartingPosition.TRIM_HORIZON,
    batch_size=5,
    bisect_batch_on_error=True,    retry_attempts=4
))



        lambda_function_consumer = python_.PythonFunction(
            self,
            "AppConsumer",
            entry="src",
            handler="handler",
            index="lambda_function_consumer.py",
            layers=[powertools_layer],
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            environment = {'SQS_URL': queue.queue_url,'table_name': demo_table.table_name,},
        )

        lambda_function_consumer.add_to_role_policy(sqsPolicy)
        lambda_function_consumer.add_to_role_policy(dynamo_db_policy)

        EventbridgeToLambda(self, 'eventbridge-delay-sqs-lambda', existing_lambda_obj = lambda_function_consumer,
                        event_rule_props=events.RuleProps(
                            schedule=events.Schedule.rate(
                                Duration.minutes(1))
                        ))


        


        
