#!/usr/bin/env python3
import os
import configparser
import os
import aws_cdk as cdk
from ecs_cdk.ecs_cdk_stack import EcsCdkStack
from aws_cdk import (
    Aspects,
    Tags,
    Environment,
)
if __name__ == "__main__":
    # --- Load Configuration ---
    config_parser = configparser.ConfigParser()
    config_parser.read(filenames="resource.config")
    #branch_name = os.getenv("SRC_BRANCH")
    branch_name = "DEV"
    config = config_parser[branch_name]

    # Initializing CDK app
    app = cdk.App()

    # --- SSM Automation Stack ---
    ssm_stack = EcsCdkStack( 
        app, 
        f"{config['app_infra_stack_name']}",
        resource_config=config,
        env=Environment(
            account=f"{config['workload_account']}",
            region=f"{config['deployment_region']}"
        )
    )
    app.synth()