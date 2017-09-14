import awspricingfull
if __name__ == '__main__':
    ec2pricing=awspricingfull.EC2Prices()
    ec2pricing.save_csv("ondemand","","awspricinglist.csv")
