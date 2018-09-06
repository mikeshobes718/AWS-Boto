#!/usr/bin/env python3

import boto3
import time
filename = time.strftime("Route53_Alerts-%Y-%m-%d.%H-%M-%S")
updates_file = time.strftime("Route53_Alerts_Updates-%Y-%m-%d.%H-%M-%S")
import os, fnmatch
import glob

rows = []
hosted_zone_id = 'Z3RHMP5QAIH3RB'
num_of_files = []

listOfFiles = os.listdir('.')
pattern = "Route53_Alerts-20*"  
for entry in listOfFiles:  
    if fnmatch.fnmatch(entry, pattern):
            num_of_files.append(entry)

try:
    firstFile = (num_of_files[0])
    count = (len(num_of_files))
except:
    count = 0

if count < 1:
    try:
        f = open("Route53_Alerts-20.txt", "w")
        f.write("Route53_Alerts-20.txt")
        print("Generated the necessary file")
        exit
    except:
        exit
elif count == 1:
    client = boto3.client('route53')
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )

    for trail_events in response['ResourceRecordSets']:
        rows.append(trail_events)

    try:
        start_record_name = response['NextRecordName']
        isTruncated = response['IsTruncated']
    except:
        start_record_name = None
        isTruncated = False    

    while(isTruncated == True and start_record_name != None):
        try:
            response = client.list_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                StartRecordName=start_record_name
            )

            for trail_events in response['ResourceRecordSets']:
                rows.append(trail_events)

            start_record_name = response['NextRecordName']
            isTruncated = response['IsTruncated']
        except:
            isTruncated = False

    thefile = open(filename + '.txt', 'w')
    for row in rows:
        thefile.write("%s\n" % row)

    thefile = os.path.basename(thefile.name)

    with open(firstFile, 'r') as file1:
        with open(thefile, 'r') as file2:
            same = set(file1).symmetric_difference(file2)

    same.discard('\n')

    with open(updates_file + '.txt', 'w') as file_out:
        for line in same:
            file_out.write(line)

    for filename in glob.glob('.'):
        os.remove(firstFile) 

elif count > 1:
    listOfFiles = os.listdir('.')  
    pattern = "Route53_Alerts-20*"  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            os.remove(entry)
else:
    exit

# for line in rows:
#     file_out.write(line)
mesg = json.dumps({
    "default": "defaultfield", # added this 
    "name": instance.title,
    "description": instance.description
})

clientSNS = boto3.client('sns')
response = clientSNS.publish(
    TopicArn='arn:aws:sns:us-east-1:924762351766:Route53_Alerts',
    Message=mesg,
    Subject='Route_53_Alerts'
)
