#!/bin/bash

zip beanstalk.zip src/beanstalk_app/beanstalk_app.py
zip lambda.zip src/lambda/lambda.py

bucket=spp-cf-artifacts

aws s3 cp beanstalk.zip s3://${bucket}/
aws s3 cp lambda.zip s3://${bucket}/

aws cloudformation create-stack --stack-name lambda-bootstrap-stack --template-body file://infra/cloudformation.json
