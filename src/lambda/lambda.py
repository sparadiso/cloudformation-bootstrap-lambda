import boto3
import os

beanstalk_client = boto3.client('elasticbeanstalk')
autoscaling_client = boto3.client('autoscaling')
cw_client = boto3.client("cloudwatch")

beanstalk_env = os.environ["BeanstalkEnv"]
queue_name = os.environ["QueueName"]


def __get_asg_name():
    resources = beanstalk_client.describe_environment_resources(EnvironmentName=beanstalk_env)
    asg_name = resources["EnvironmentResources"]["AutoScalingGroups"][0]["Name"]
    return asg_name


def __get_scaling_policies(asg_name):
    policies = autoscaling_client.describe_policies(AutoScalingGroupName=asg_name)["ScalingPolicies"]
    scale_up_policy = [x for x in policies if x["ScalingAdjustment"] > 0][0]
    scale_down_policy = [x for x in policies if x["ScalingAdjustment"] < 0][0]

    return (scale_up_policy, scale_down_policy)


def __create_alarms(scale_up_policy, scale_down_policy):
    cw_client.put_metric_alarm(
        AlarmName="SQS Messages Available",
        AlarmActions=[scale_up_policy["PolicyARN"]],
        MetricName="ApproximateNumberOfMessagesVisible",
        Namespace="AWS/SQS",
        Dimensions=[{"Name": "QueueName", "Value": queue_name}],
        Period=60,
        EvaluationPeriods=1,
        Threshold=0,
        ComparisonOperator="GreaterThanThreshold",
        Statistic="Maximum"
    )

    cw_client.put_metric_alarm(
        AlarmName="No SQS messages available",
        AlarmActions=[scale_down_policy["PolicyARN"]],
        MetricName="ApproximateNumberOfMessagesVisible",
        Namespace="AWS/SQS",
        Dimensions=[{"Name": "QueueName", "Value": queue_name}],
        Period=60,
        EvaluationPeriods=5,
        Threshold=0,
        ComparisonOperator="EqualToThreshold",
        Statistic="Maximum"
    )


def main(event, context):
    try:
        asg_name = __get_asg_name()
        scale_up_policy, scale_down_policy = __get_scaling_policies(asg_name)
        __create_alarms(scale_up_policy, scale_down_policy)
    except:
        pass
