#!/usr/bin/env python3
import os

import aws_cdk as cdk

from pantrydb_stack import PantryDBStack

app = cdk.App()
PantryDBStack(
    app,
    "PantryDBStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
