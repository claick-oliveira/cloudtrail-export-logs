# Import the SDK
import boto3
import json
import argparse
import os

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--startime", help="add start time")
parser.add_argument("-e", "--endtime", help="add end time")
parser.add_argument("-r", "--region", help="add region")
parser.add_argument("-a", "--accountid", help="add account id")

args = parser.parse_args()
set_startime = args.startime
set_endtime = args.endtime
set_region = args.region
set_accountid = args.accountid

# Clients
clientCT = boto3.client('cloudtrail', region_name=set_region)


def get_event():
  try:
    directory = f'./output/{set_accountid}/{set_region}'
    # Check whether the specified directory exists or not
    isExist = os.path.exists(directory)
    if not isExist:
      os.makedirs(directory)
    sub_startime = re.sub(r':| |, ', '-', set_startime)
    sub_endtime = re.sub(r':| |, ', '-', set_endtime)
    file_name = f'cloudtrail-from-{sub_startime}-to-{sub_endtime}-ID-{set_accountid}-region-{set_region}.txt'
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
