import json
import boto3
from prettytable import PrettyTable

elbv2_client = boto3.client('elbv2')


def get_load_balancer_details(lb_name):
    result_table = PrettyTable()
    result_table.field_names = [
        "LoadBalancerName", "ListenerArn", "RulePriority", 
        "TargetGroupArn", "TrafficWeight", "Condition", 
        "InstanceId", "HealthStatus"
    ]

    # Fetch load balancer ARN for the given name
    try:
        load_balancers = elbv2_client.describe_load_balancers(
            Names=[lb_name]
        )['LoadBalancers']
    except elbv2_client.exceptions.LoadBalancerNotFoundException:
        return f"Load balancer '{lb_name}' not found."

    lb_arn = load_balancers[0]['LoadBalancerArn']

    # Fetch listeners for the load balancer
    listeners = elbv2_client.describe_listeners(LoadBalancerArn=lb_arn)['Listeners']

    for listener in listeners:
        listener_arn = listener['ListenerArn']

        # Fetch rules for each listener
        rules = elbv2_client.describe_rules(ListenerArn=listener_arn)['Rules']

        for rule in rules:
            rule_priority = rule['Priority']
            conditions = ", ".join(
                condition.get('Values', ['-'])[0] for condition in rule['Conditions']
            )

            # Handle multiple target groups under the same rule
            for action in rule['Actions']:
                if action['Type'] == 'forward':
                    target_group_arn = action.get('TargetGroupArn', '-')
                    traffic_weight = action.get('Weight', 'N/A')

                    # Fetch health details for each target group
                    if target_group_arn != '-':
                        health_descriptions = elbv2_client.describe_target_health(
                            TargetGroupArn=target_group_arn
                        )['TargetHealthDescriptions']

                        for target in health_descriptions:
                            instance_id = target['Target']['Id']
                            health_status = target['TargetHealth']['State']
                            result_table.add_row([
                                lb_name, listener_arn, rule_priority,
                                target_group_arn, traffic_weight, conditions,
                                instance_id, health_status
                            ])
                    else:
                        result_table.add_row([
                            lb_name, listener_arn, rule_priority,
                            target_group_arn, traffic_weight, conditions,
                            "-", "-"
                        ])

    return result_table


def lambda_handler(event, context):
    # Example: Get Load Balancer name from event
    lb_name = event.get("LoadBalancerName", "default-lb-name")

    # Fetch and display load balancer details
    result = get_load_balancer_details(lb_name)

    # Return the table as a string
    return {
        "statusCode": 200,
        "body": str(result)
    }
