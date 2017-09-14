#!/usr/bin/env python

import csv
import sys
import json


def read_EC2_ondemand_instance_prices(number, region, flavor, os):
	if number <=0:
		return 0
	ifile  = open("awspricinglist.csv", "r")

	reader = csv.reader(ifile)

	unit_cost = 0
	rownum = 0
	for row in reader:

	    if rownum != 0:
	    	if row[0]==region and row[1] ==flavor and row[2]==os:
		    	unit_cost = row[3]
		     	break

	    rownum += 1

	ifile.close()
	cost = float(unit_cost) * int(number)
	return cost

def aws_storage_prices(region, storage_size):

	config = json.loads(open("pricing-storage-s3.json").read())
	storage_cost = 0
	monthly_Storage_Cost = 0
	#print [0]['tiers'][0]['storageTypes'][0]['prices']['USD']
	data_centers = config['config']['regions']

	for data_center in data_centers:

		if region==data_center['region']:
			storage_cost = data_center['tiers'][0]['storageTypes'][0]['prices']['USD']
			break

	#print storage_cost

	return float(storage_cost) * int(storage_size)
		#print region['region'], region['tiers'][0]['storageTypes'][0]['prices']['USD']
	#print monthly_Storage_Cost


def gce_price(zone, machine_type, storage_size):
	return 0

if __name__ == "__main__":
	'''
	if len(sys.argv) <= 5:

		print "Usage:[number of instances] [region] [flavor] [os] [storage-size]"


	INSTANCE_NUMBER = sys.argv[1]
	REGION = sys.argv[2];
	FLAVOR = sys.argv[3];
	OS = sys.argv[4]
	STORAGE_SIZE = sys.argv[5]
	'''
	machine_types = ["t2.nano","t2.micro","t2.large","m4.large","m3.large","c4.large","c3.large","r3.large","m4.2xlarge", "m4.4xlarge","m3.2xlarge",
		"c4.2xlarge", "c4.4xlarge","c4.8xlarge","c3.2xlarge","c3.4xlarge","c3.8xlarge","g2.2xlarge","g2.8xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
		"d2.2xlarge","d2.4xlarge","d2.8xlarge "]

	aws_regions = ["us-east-1","us-west-1","us-west-2","eu-west-1","eu-central-1","ap-southeast-1","ap-northeast-1","ap-southeast-2","ap-northeast-2"
				,"sa-east-1","us-gov-west-1"]

	platforms = ["linux","rhel", "sles","mswin","mswinSQL","mswinSQLWeb"]


	user_choice = input("Please select cloud provider: \n1) Amazon Web Services\n2) Google Cloud\n")

	if user_choice==1:
		#selects regions
		region_option = "Please, select region: (0-"+str(len(aws_regions)-1)+")\n"
		for region in aws_regions:

			region_option += str(aws_regions.index(region))+") "+region + "\n"

		chosen_region = input(region_option)

		#type number of instances required
		intance_number = input("Please type number of instances: \n")

		#selects machine types for AWS
		flavor_options = "Please, select machine type: (0-"+str(len(machine_types)-1)+")\n"
		for machine in machine_types:

			flavor_options += str(machine_types.index(machine))+") "+machine+"\n"

		chosen_flavor = input(flavor_options)

		#selects operating systems types for AWS
		os_options = "Please, select OS: (0-"+str(len(platforms)-1)+")\n"

		for os in platforms:

			os_options += str(platforms.index(os))+") "+os+"\n"

		chosen_os = input(os_options)

		storage_size = input("Please, enter storage size: ")


		price = read_EC2_ondemand_instance_prices(intance_number, aws_regions[chosen_region], machine_types[chosen_flavor], platforms[chosen_os]);

		storage_price  = aws_storage_prices(aws_regions[chosen_region], storage_size)

		#print storage_price
		print "You selected: "+str(intance_number)+ ", "+str(aws_regions[chosen_region])+", "+str(machine_types[chosen_flavor])+", "+str(platforms[chosen_os])+ ", "+str(storage_size)
		print "The hourly price of the instance:  \t$%.3f "% (price/int(intance_number))

		total_price = price * (((720*4) + (744*7) + (28*24*1))/12)
		#print total_price
		print "Cost of storage: \t$%.2f " % (storage_price)
		print "Monthly cost of the instance + storage = \t$%.2f " %( total_price + storage_price);
		print "\n\n"

		#print aws_storage_prices(REGION, STORAGE_SIZE)
	else:

		print "Estimates on Google Cloud is coming soon ...."
