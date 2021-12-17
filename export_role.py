# Import the SDK
import boto3
import json
import argparse
import os
import re

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--startime", help="add start time")
parser.add_argument("-e", "--endtime", help="add end time")
parser.add_argument("-r", "--region", help="add region")
parser.add_argument("-a", "--accountid", help="add account id")
parser.add_argument("-arn", "--arn", help="add arn")

args = parser.parse_args()
set_startime = args.startime
set_endtime = args.endtime
set_region = args.region
set_accountid = args.accountid
set_arn = args.arn

# create an STS client object that represents a live connection to the
# STS service
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
assumed_role_object=sts_client.assume_role(
    RoleArn=set_arn,
    RoleSessionName="AssumeRoleSession1"
)

# From the response that contains the assumed role, get the temporary
# credentials that can be used to make subsequent API calls
credentials=assumed_role_object['Credentials']

# Clients
clientCT = boto3.client(
  'cloudtrail',
  region_name=set_region,
  aws_access_key_id=credentials['AccessKeyId'],
  aws_secret_access_key=credentials['SecretAccessKey'],
  aws_session_token=credentials['SessionToken'],
)


def get_event():
  try:
    directory = f'./output/{set_accountid}/{set_region}'
    # Check whether the specified directory exists or not
    isExist = os.path.exists(directory)
    if not isExist:
      os.makedirs(directory)
    sub_startime = re.sub(r':| |, ', '-', set_startime)
    sub_endtime = re.sub(r':| |, ', '-', set_endtime)
    sub_arn = set_arn.split("/")[-1]
    file_name = f'cloudtrail-from-{sub_startime}-to-{sub_endtime}-ID-{set_accountid}-region-{set_region}-role-{sub_arn}.txt'
    textfile = open(
      f'{directory}/{file_name}', 'w'
    )
    paginator = clientCT.get_paginator('lookup_events')
    response_iterator_CT = paginator.paginate(
      StartTime=set_startime,
      EndTime=set_endtime,
      PaginationConfig={
        'PageSize': 50,
      }
    )
    for event in response_iterator_CT:
      for key, value in event.items():
        if key == "Events":
          mylist = value
          if mylist == []:
            continue
          else:
            for v in mylist:
              CTevent = (v["CloudTrailEvent"])
              JSONEvent = json.loads(CTevent)
              v["CloudTrailEvent"] = JSONEvent
              textfile.write(json.dumps(v, default=str) + '\n')

  except Exception as error:
      print("\n"+str(error))


get_event()
