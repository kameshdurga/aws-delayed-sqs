import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.python_cdk_stack import CdkStack


def test_lambda_function_created():
    app = core.App()
    stack = CdkStack(app, "cdk")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function", {"Runtime": "python3.9"})
