#!/usr/bin/python

import urllib2
import csv
import re
try:
    import simplejson as json
except ImportError:
    import json
import os

class AWSPrices(object):

    CURRENCY = "USD"

    REGIONS = [
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "eu-west-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "sa-east-1",
    "eu-central-1",
    "us-gov-west-1"
    ]

    JSON_NAME_TO_REGIONS_API = {
    "us-east" : "us-east-1",
    "us-east-1" : "us-east-1",
    "us-west" : "us-west-1",
    "us-west-1" : "us-west-1",
    "us-west-2" : "us-west-2",
    "eu-ireland" : "eu-west-1",
    "eu-west-1" : "eu-west-1",
    "apac-sin" : "ap-southeast-1",
    "ap-southeast-1" : "ap-southeast-1",
    "ap-southeast-2" : "ap-southeast-2",
    "apac-syd" : "ap-southeast-2",
    "apac-tokyo" : "ap-northeast-1",
    "ap-northeast-1" : "ap-northeast-1",
    "ap-northeast-2" : "ap-northeast-2",
    "sa-east-1" : "sa-east-1",
    "eu-central-1":"eu-central-1",
    "us-gov-west-1":"us-gov-west-1",
    "eu-frankfurt":"eu-central-1"
    }

    def load_data(self,url):
        f = urllib2.urlopen(url).read()
        f = re.sub("/\\*[^\x00]+\\*/", "", f, 0, re.M)
        f = re.sub("([a-zA-Z0-9]+):", "\"\\1\":", f)
        f = re.sub(";", "\n", f)
        f = re.sub("callback\(", "", f)
        f = re.sub("\)$", "", f)
        data = json.loads(f)
        return data


    def none_as_string(self,v):
            if not v:
                return ""
            else:
                return v


    def get_ondemand_instances_prices(self):

        raise NotImplementedError( "Should have implemented this" )

    def return_json(self,u):
        if u not in ["ondemand"]:
            print("Function requires 1 parameter. Possible values:"
                  "\"ondemand\".")
        else:
            if u == "ondemand":
                data = self.get_ondemand_instances_prices()
            return (json.dumps(data))



class EC2Prices(AWSPrices):

    INSTANCES_ON_DEMAND_LINUX_URL =("http://a0.awsstatic.com/pricing/1/ec2/"+
    "linux-od.min.js")
    INSTANCES_ON_DEMAND_RHEL_URL =("http://a0.awsstatic.com/pricing/1/ec2/"+
    "rhel-od.min.js")
    INSTANCES_ON_DEMAND_SLES_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "sles-od.min.js")
    INSTANCES_ON_DEMAND_WINDOWS_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "mswin-od.min.js")
    INSTANCES_ON_DEMAND_WINSQL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "mswinSQL-od.min.js")
    INSTANCES_ON_DEMAND_WINSQLWEB_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "mswinSQLWeb-od.min.js")

    PG_INSTANCES_ON_DEMAND_LINUX_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/linux-od.min.js")
    PG_INSTANCES_ON_DEMAND_RHEL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/rhel-od.min.js")
    PG_INSTANCES_ON_DEMAND_SLES_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/sles-od.min.js")
    PG_INSTANCES_ON_DEMAND_WINDOWS_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/mswin-od.min.js")
    PG_INSTANCES_ON_DEMAND_WINSQL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/mswinSQL-od.min.js")
    PG_INSTANCES_ON_DEMAND_WINSQLWEB_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/mswinSQLWeb-od.min.js")

    INSTANCES_RESERVED_LINUX_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "ri-v2/linux-unix-shared.min.js")
    INSTANCES_RESERVED_RHEL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "ri-v2/red-hat-enterprise-linux-shared.min.js")
    INSTANCES_RESERVED_SLES_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "ri-v2/suse-linux-shared.min.js")
    INSTANCES_RESERVED_WINDOWS_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "ri-v2/windows-shared.min.js")
    INSTANCES_RESERVED_WINSQL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "ri-v2/windows-with-sql-server-standard-shared.min.js")
    INSTANCES_RESERVED_WINSQLWEB_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "ri-v2/windows-with-sql-server-web-shared.min.js")

    PG_INSTANCES_RESERVED_LINUX_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/ri-v2/linux-unix-shared.min.js")
    PG_INSTANCES_RESERVED_RHEL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/ri-v2/red-hat-enterprise-linux-shared.min.js")
    PG_INSTANCES_RESERVED_SLES_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/ri-v2/suse-linux-shared.min.js")
    PG_INSTANCES_RESERVED_WINDOWS_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/ri-v2/windows-shared.min.js")
    PG_INSTANCES_RESERVED_WINSQL_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/ri-v2/windows-with-sql-server-standard-shared.min.js")
    PG_INSTANCES_RESERVED_WINSQLWEB_URL = ("http://a0.awsstatic.com/pricing/1/ec2/"+
    "previous-generation/ri-v2/windows-with-sql-server-web-shared.min.js")


    INSTANCES_ONDEMAND_OS_TYPE_BY_URL = {
        INSTANCES_ON_DEMAND_LINUX_URL : "linux",
        INSTANCES_ON_DEMAND_RHEL_URL : "rhel",
        INSTANCES_ON_DEMAND_SLES_URL : "sles",
        INSTANCES_ON_DEMAND_WINDOWS_URL : "mswin",
        INSTANCES_ON_DEMAND_WINSQL_URL : "mswinSQL",
        INSTANCES_ON_DEMAND_WINSQLWEB_URL : "mswinSQLWeb",
        PG_INSTANCES_ON_DEMAND_LINUX_URL : "linux",
        PG_INSTANCES_ON_DEMAND_RHEL_URL : "rhel",
        PG_INSTANCES_ON_DEMAND_SLES_URL : "sles",
        PG_INSTANCES_ON_DEMAND_WINDOWS_URL : "mswin",
        PG_INSTANCES_ON_DEMAND_WINSQL_URL : "mswinSQL",
        PG_INSTANCES_ON_DEMAND_WINSQLWEB_URL : "mswinSQLWeb"
    }

    INSTANCES_RESERVED_OS_TYPE_BY_URL = {

        INSTANCES_RESERVED_LINUX_URL : "linux",
        INSTANCES_RESERVED_RHEL_URL : "rhel",
        INSTANCES_RESERVED_SLES_URL : "sles",
        INSTANCES_RESERVED_WINDOWS_URL :  "mswin",
        INSTANCES_RESERVED_WINSQL_URL : "mswinSQL",
        INSTANCES_RESERVED_WINSQLWEB_URL : "mswinSQLWeb",
        PG_INSTANCES_RESERVED_LINUX_URL : "linux",
        PG_INSTANCES_RESERVED_RHEL_URL : "rhel",
        PG_INSTANCES_RESERVED_SLES_URL : "sles",
        PG_INSTANCES_RESERVED_WINDOWS_URL :  "mswin",
        PG_INSTANCES_RESERVED_WINSQL_URL : "mswinSQL",
        PG_INSTANCES_RESERVED_WINSQLWEB_URL : "mswinSQLWeb"
    }

    def get_ondemand_instances_prices(self):
        print "Extracting pricing data from aws api ..."
        currency = self.CURRENCY

        urls = [
            self.INSTANCES_ON_DEMAND_LINUX_URL,
            self.INSTANCES_ON_DEMAND_RHEL_URL,
            self.INSTANCES_ON_DEMAND_SLES_URL,
            self.INSTANCES_ON_DEMAND_WINDOWS_URL,
            self.INSTANCES_ON_DEMAND_WINSQL_URL,
            self.INSTANCES_ON_DEMAND_WINSQLWEB_URL,
            self.PG_INSTANCES_ON_DEMAND_LINUX_URL,
            self.PG_INSTANCES_ON_DEMAND_RHEL_URL,
            self.PG_INSTANCES_ON_DEMAND_SLES_URL,
            self.PG_INSTANCES_ON_DEMAND_WINDOWS_URL,
            self.PG_INSTANCES_ON_DEMAND_WINSQL_URL,
            self.PG_INSTANCES_ON_DEMAND_WINSQLWEB_URL
        ]

        result_regions = []
        result = {
            "config" : {
                "currency" : currency,
                "unit" : "perhr"
            },
            "regions" : result_regions
        }

        for u in urls:

            data = self.load_data(u)
            if ("config" in data and data["config"] and "regions"
                in data["config"] and data["config"]["regions"]):
                for r in data["config"]["regions"]:
                    if "region" in r and r["region"]:

                        region_name = r["region"]
                        instance_types = []
                        if "instanceTypes" in r:
                            for it in r["instanceTypes"]:
                                if "sizes" in it:
                                    for s in it["sizes"]:
                                        instance_type = s["size"]

                                        for price_data in s["valueColumns"]:
                                            price = None
                                            try:
                                                price =float(re.sub("[^0-9\.]", "",
                                                                    price_data["prices"][currency]))
                                            except:
                                                price = None
                                            _type = instance_type
                                            instance_types.append({
                                                "type" : _type,
                                                "os" : price_data["name"],
                                                "price" : price
                                            })

                            result_regions.append({
                                "region" : region_name,
                                "instanceTypes" : instance_types
                            })

        return result

    def save_csv(self,u,path=os.getcwd()+"\\",name=None):

        if u not in ["ondemand"]:
            print("Function requires 1 parameter. Possible values:"
                  "\"ondemand\".")

        elif u == "ondemand":
            if name is None:
                name="aws_ec2_ondemand_pricing.csv"
            data = self.get_ondemand_instances_prices()
            writer = csv.writer(open(path+name, 'wb'))
            print "Writing date to file ..."
            writer.writerow(["region","type","os","price"])
            for r in data["regions"]:
                region_name = r["region"]
                for it in r["instanceTypes"]:
                    writer.writerow([region_name,it["type"],it["os"],self.none_as_string(it["price"])])
        print "Data successfully written to file!"
