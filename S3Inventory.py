#!/usr/bin/python

import time
filename = time.strftime("s3_Inventory-%Y-%m-%d.%H-%M-%S")
from datetime import datetime
print("Generating file: " + filename + ".csv")
print("Please wait......")
import sys
import boto3
import botocore
import pprint as pp
import subprocess
import csv

startTime = datetime.now()

client = boto3.client('s3')

response = client.list_buckets()

#fieldnames = ['name', 'creationDate', 'accessLogEnabled', 'encryptionSetting', 'versioningEnabled', 'classification', 'costCenter', 'environment']

rows = []
rows.append("Bucket Name"+ "," + "Bucket Creation Date" + "," + "Access Log Enabled" + "," + "Encryption Setting" + "," + "Versioning Enabled" + "," + "Classification" + "," + "Cost Center" + "," + "Environment")

for bucket in response['Buckets']:

        bucket_name = bucket['Name']

        bucket_create_date =  bucket['CreationDate']
        bucket_create_date = bucket_create_date.strftime('%m/%d/%Y')

        accessLogEnabled = client.get_bucket_logging(Bucket='tagmeplease')
        if 'LoggingEnabled' in accessLogEnabled:
            accessLogEnabled = "LoggingEnabled"
        else:
            accessLogEnabled = "LoggingDisabled"

        try:
            encryption_info = client.get_bucket_encryption(Bucket='cf-templates-m9a6k1lajhj5-us-west-2').get("ServerSideEncryptionConfiguration").get("Rules")
            encryptionSetting = encryption_info

            res  = {}
            for line in encryptionSetting:
                res.update(line)
                encryptionSetting = (res.get("ApplyServerSideEncryptionByDefault").get("SSEAlgorithm"))
        except:
            encryptionSetting = "Encryption Disabled"

        versioningEnabled = client.get_bucket_versioning(Bucket=bucket_name)
        versioningEnabled = versioningEnabled.get("Status")
        if versioningEnabled is None:
            versioningEnabled = "VersioningDisabled"

        #Classificaton
        try:
            classification = client.get_bucket_tagging(Bucket=bucket_name).get("TagSet")
            attrs = {}
            for value in classification:
                attrs[value["Key"]] = value["Value"]
            if 'classification' in attrs:
                classification = (attrs['classification'])
            else:
                classification = "NoClassification"
        except:
            classification = "NoClassification"

        #Cost Center
        try:
            costCenter = client.get_bucket_tagging(Bucket=bucket_name).get("TagSet")
            attrs = {}
            for value in costCenter:
                attrs[value["Key"]] = value["Value"]
            if 'costCenter' in attrs:
                costCenter = (attrs['costCenter'])
            else:
                costCenter = "NoCostCenter"
        except:
            costCenter = "NoCostCenter"
   
        #Environment
        try:
            environment = client.get_bucket_tagging(Bucket=bucket_name).get("TagSet")
            attrs = {}
            for value in environment:
                attrs[value["Key"]] = value["Value"]
            if 'environment' in attrs:
                environment = (attrs['environment'])
            else:
                environment = "NoEnvironment"
        except:
            environment = "NoEnvironment"
        #print()

        csv_input = bucket_name + "," + bucket_create_date + "," + accessLogEnabled + "," + encryptionSetting + "," + versioningEnabled + "," + classification + "," + costCenter + "," + environment
        rows.append(csv_input)
        #print (rows)
        #print()

thefile = open(filename + '.csv', 'x')
for item in rows:
  thefile.write("%s\n" % item)

subprocess.run(["clear"])

print("Please open: " + filename)
runtime = (datetime.now() - startTime)
#print("Total runtime: " + runtime) #mod on train
print("Done!")
