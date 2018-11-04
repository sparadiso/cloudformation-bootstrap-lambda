# Cloudformation with bootstrap lambda
Prototype example demonstrating how to do last-mile customizations via bootstrap lambda defined in a cloudformation template. The basic approach is to define a custom resource compatible lambda function that takes in information about the created resources (beanstalk env name, e.g) in order to find those resources via boto3 and apply any customized configurations. The example used here is to apply a custom scale-up/down policy that triggers on an SQS metric, which is not available from beanstalk out of the box.

# Requirements

You'll need an AWS account set up and activated credentials with Admin privileges (this example doesn't engage meaningfully with permissions - it's just meant to be deployed and torn down).

Since beanstalk requires a URL for artifacts, you'll need to set up an S3 bucket that will be referenced later.

Finally, the deploy script (and cleanup command below) requires the [awscli](https://docs.aws.amazon.com/cli/latest/userguide/installing.html), which can be installed with pip:

```bash
$> pip install awscli
```

# Usage

To deploy the stack, simply run:
```bash
$> ./infra/deploy.sh my_artifact_bucket
```

This will create a stack called `lambda-bootstrap-stack` in your AWS account and deploy a dummy beanstalk environment (and lambda).

# Cleanup

When you're done inspecting the results, you can clean up by running:
```bash
$> aws cloudformation delete-stack --stack-name lambda-bootstrap-stack
```
