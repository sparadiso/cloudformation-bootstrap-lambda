# Cloudformation with bootstrap lambda
Toy example with a bootstrap lambda function defined in a cloudformation template that triggers and applies a custom autoscaling policy (scale up when SQS messages are available) to a beanstalk-generated autoscaling group. Useful for simple async worker configurations.
