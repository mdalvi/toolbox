import boto3


def send_notification(topic_arn, subject, message_body):
    sns_client = boto3.client('sns')
    sns_client.publish(TopicArn=topic_arn, Message=message_body, Subject=subject)
