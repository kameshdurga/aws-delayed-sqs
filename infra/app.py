#!/usr/bin/env python3
import aws_cdk as cdk
from python_cdk_stack import CdkStack
import os

app = cdk.App()
lambdafun = CdkStack(app, "PythonCdkStack",env=cdk.Environment(
    region="us-east-2"))

app.synth()
