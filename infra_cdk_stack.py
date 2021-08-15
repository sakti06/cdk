from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core
)


class InfraCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "InfraCdkQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "InfraCdkTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))

        vpc = ec2.Vpc(
         self, "TestVPC",
         cidr="10.0.0.0/16",
         max_azs=2,
         nat_gateways=1,
         subnet_configuration=[
                ec2.SubnetConfiguration(name="DMZ", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="APP", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE),
                ec2.SubnetConfiguration(name="DB", cidr_mask=24, subnet_type=ec2.SubnetType.ISOLATED)
             ]
         ) 