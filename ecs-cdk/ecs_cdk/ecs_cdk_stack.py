from aws_cdk import (
    # Duration,
    Stack,
    aws_ssm as ssm, 
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct

class EcsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, resource_config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # IAM Role for Automation
        automation_role = iam.Role(
            self, "SSMAutomationRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ssm.amazonaws.com"),
                iam.AccountPrincipal(resource_config['ssm_target_account_ids'])
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonSSMAutomationRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess")
            ]
        )
        # ECS: Stop All Services
        ssm.CfnDocument(
            self, "SSMDocumentStopAllECS",
            name="Stop-All-ECS-Services",
            document_type="Automation",
            content={
                "schemaVersion": "0.3",
                "description": "Stops all ECS services in a cluster",
                "parameters": {
                    "ClusterName": {"type": "String", "default": resource_config['ecs_cluster']},
                    "AutomationAssumeRole": {"type": "String", "default": automation_role.role_arn}
                },
                "assumeRole": "{{ AutomationAssumeRole }}",
                "mainSteps": [
                    {
                        "name": "listServices",
                        "action": "aws:executeAwsApi",
                        "inputs": {
                            "Service": "ECS",
                            "Api": "ListServices",
                            "cluster": "{{ ClusterName }}"
                        },
                        "outputs": [
                            {
                                "Name": "ServiceArns",
                                "Selector": "$.serviceArns",
                                "Type": "StringList"
                            }
                        ]
                    },
                    {
                        "name": "stopServices",
                        "action": "aws:executeScript",
                        "inputs": {
                            "Runtime": "python3.8",
                            "Handler": "StopAllEcsServices",
                            "InputPayload": {
                                "cluster": "{{ ClusterName }}",
                                "serviceArns": "{{ listServices.ServiceArns }}"
                            },
                            "Script": "def StopAllEcsServices(event, context):\n  import boto3\n  ecs = boto3.client('ecs')\n  for service in event['serviceArns']:\n    ecs.update_service(\n      cluster=event['cluster'],\n      service=service,\n      desiredCount=0\n    )\n    return {\"status\": \"success\"}\n",
                          }
                    },
                    
                ]
            }
        )
        ssm.CfnDocument(
            self, "SSMDocumentStopPerECSService",
            name="Stop-Per-ECS-Services",
            document_type="Automation",
            content={
                "schemaVersion": "0.3",
                "description": "Stops all ECS services in a cluster",
                "parameters": {
                    "ClusterName": {"type": "String", "default": resource_config['ecs_cluster']},
                    "ServiceArn" : {"type": "String", "default": resource_config['ecs_service_arn']},
                    "AutomationAssumeRole": {"type": "String", "default": automation_role.role_arn}
                },
                "assumeRole": "{{ AutomationAssumeRole }}",
                "mainSteps": [
                    {
                          "name": "stopPerServices",
                          "action": "aws:executeScript",
                          "inputs": {
                            "Script": "def StopPerECSService(event, context):\n  import boto3\n  ecs = boto3.client('ecs')\n  ecs.update_service(\n        cluster=event['cluster'],\n        service=event['serviceArns'],\n        desiredCount=0\n  )\n  return {\"status\": \"success\"}",
                            "Runtime": "python3.8",
                            "InputPayload": {
                              "cluster": "{{ ClusterName }}",
                              "serviceArns": "{{ ServiceArn }}"
                            },
                            "Handler": "StopPerECSService"
                          }
                        }
                    
                ]
            }
        )
