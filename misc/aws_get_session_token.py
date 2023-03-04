#!/bin/python

import boto3
import sys
import os

aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
user_arn = "arn:aws:iam::917894928123:mfa/<user>"
session_duration = 43200
owaCode = ''

try:
    owaCode = sys.argv[1]

except IndexError as e:
    print('Missing AWS MFA code!')

try:
    client = boto3.client(
        'sts',
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_secret_key
    )
    resp = client.get_session_token(
        DurationSeconds=session_duration,
        SerialNumber=user_arn,
        TokenCode=owaCode
    )
    session_id = resp['Credentials']['SessionToken']
    print(session_id)

except Exception as e:
    print(e)
