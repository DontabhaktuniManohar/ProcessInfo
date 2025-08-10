import boto3
import datetime
import time
import logging
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logs = boto3.client('logs')
cloudwatch = boto3.client('cloudwatch')

# Configurable threshold and alarm settings
THRESHOLD = int(os.environ.get('ALARM_THRESHOLD', '100'))
ALARM_PREFIX = os.environ.get('ALARM_PREFIX', 'PausedCountAlarm-')
NAMESPACE = 'Custom/SequencePaused'
METRIC_NAME = 'PausedCount'
PERIOD = 300
EVALUATION_PERIODS = 1

def alarm_exists(alarm_name):
    """Check if an alarm already exists."""
    response = cloudwatch.describe_alarms(AlarmNames=[alarm_name])
    return len(response['MetricAlarms']) > 0

def create_alarm(recipient):
    """Create CloudWatch alarm for a recipient."""
    alarm_name = f"{ALARM_PREFIX}{recipient}"
    
    if alarm_exists(alarm_name):
        logger.info(f"🔁 Alarm already exists for {recipient}")
        return
    
    cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName=METRIC_NAME,
        Namespace=NAMESPACE,
        Dimensions=[{'Name': 'Recipient', 'Value': recipient}],
        Statistic='Sum',
        Period=PERIOD,
        EvaluationPeriods=EVALUATION_PERIODS,
        Threshold=THRESHOLD,
        ComparisonOperator='GreaterThanThreshold',
        ActionsEnabled=False,
        AlarmDescription=f"Alert when PausedCount for {recipient} exceeds {THRESHOLD}",
        TreatMissingData='notBreaching'
    )
    logger.info(f"✅ Created alarm for {recipient}")

def lambda_handler(event, context):
    try:
        logger.info("Lambda function started")

        query = """
        fields @timestamp, @message, @logStream, @log, data, toRecipient
        | filter @message like /sequencePauseNotification/ and not isempty(data)
        | stats count(*) as rteCount by toRecipient, bin(5m)
        | sort rteCount desc
        | limit 10000
        """
        log_group = "/aws/lambda/dcercrc"
        logger.info(f"Running query on log group: {log_group}")

        start_query = logs.start_query(
            logGroupName=log_group,
            startTime=int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp()),
            endTime=int(datetime.datetime.now().timestamp()),
            queryString=query
        )

        query_id = start_query['queryId']
        logger.info(f"Started Logs Insights query with ID: {query_id}")

        # Wait for query to complete
        logger.info("Waiting for query to complete...")
        time.sleep(35)

        response = logs.get_query_results(queryId=query_id)
        status = response.get('status')
        results = response.get('results', [])

        logger.info(f"Query status: {status}")
        logger.info(f"Number of results returned: {len(results)}")

        if not results:
            logger.warning("No results found in query")
            return {
                'statusCode': 204,
                'body': 'No data found'
            }

        for result in results:
            recipient = next((field['value'] for field in result if field['field'] == 'toRecipient'), 'Unknown')
            count_str = next((field['value'] for field in result if field['field'] == 'rteCount'), '0')
            count = int(count_str) if count_str.isdigit() else 0

            logger.info(f"Recipient: {recipient}, Count: {count}")

            # Push metric to CloudWatch
            cloudwatch.put_metric_data(
                Namespace=NAMESPACE,
                MetricData=[{
                    'MetricName': METRIC_NAME,
                    'Dimensions': [{'Name': 'Recipient', 'Value': recipient}],
                    'Timestamp': datetime.datetime.utcnow(),
                    'Value': count,
                    'Unit': 'Count'
                }]
            )
            logger.info(f"Pushed metric to CloudWatch for {recipient}")

            # Create alarm if needed
            if count > THRESHOLD:
                create_alarm(recipient)

        logger.info("Lambda execution completed successfully")
        return {
            'statusCode': 200,
            'body': 'Metrics and alarms processed successfully'
        }

    except Exception as e:
        logger.error("Exception occurred during Lambda execution", exc_info=True)
        return {
            'statusCode': 500,
            'body': f"Error occurred: {str(e)}"
        }
