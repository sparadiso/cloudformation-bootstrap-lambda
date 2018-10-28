#!/bin/bash

bucket=$1

# Zip the artifacts and upload them to s3
zip -j beanstalk.zip src/beanstalk_app/beanstalk_app.py
zip -j lambda.zip src/lambda/lambda.py
zip -j lambda.zip src/lambda/cfnresponse.py

aws s3 cp beanstalk.zip s3://${bucket}/
aws s3 cp lambda.zip s3://${bucket}/

aws cloudformation create-stack \
--stack-name lambda-bootstrap-stack \
--template-body file://infra/cloudformation.json \
--capabilities CAPABILITY_IAM
