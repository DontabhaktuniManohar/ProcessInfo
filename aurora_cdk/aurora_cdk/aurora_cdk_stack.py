from aws_cdk import (
    # Duration,
    Stack,
    aws_ssm as ssm, 
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct


class AuroraCdkStack(Stack):

     def __init__(self, scope: Construct, construct_id: str, resource_config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # IAM Role for Automation
        automation_role = iam.Role(
            self, "SSMAutomationRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ssm.amazonaws.com")
            ),
         
        )
        # Add inline policy for RDS failover and promotion actions
        automation_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "rds:FailoverDBCluster",
                    "rds:PromoteReadReplicaGlobalCluster",
                    "rds:FailoverGlobalCluster",
                    "rds:DescribeGlobalClusters",
                    "rds:DescribeDBClusters",
                    "rds:DescribeDBInstances"
                ],
                resources=["*"]  # Or restrict to specific ARNs
            )
        )

        ssm.CfnDocument(
            self, "SSMDocumentFailoverDBCluster",
            name="FailoverDBCluster-MultiAZ",
            document_type="Automation",
            content={
                "schemaVersion": "0.3",
                "description": "FailoverDBCluster in MultiAZ ",
                "parameters": {
                    "DBClusterIdentifier": {"type": "String", "default": resource_config['aurora_cluster_id']},
                    "AutomationAssumeRole": {"type": "String", "default": automation_role.role_arn}
                },
                "assumeRole": "{{ AutomationAssumeRole }}",
                "mainSteps": [
                        {
                          "name": "FailoverDBCluster",
                          "action": "aws:executeAwsApi",
                          "inputs": {
                            "Service": "rds",
                            "Api": "FailoverDBCluster",
                            "DBClusterIdentifier": "{{ DBClusterIdentifier }}"
                          }
                        }
                    ]
                }
        )    