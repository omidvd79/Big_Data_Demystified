import sys, getopt
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi

###init
access_token = 'xyz'
app_secret = 'secret'
ad_account_id = 'act_123'
api = FacebookAdsApi.init(access_token=access_token,app_secret=app_secret)
output_json=''
start_date='1970-02-01'
usage = 'script.py --start_date 1930-01-01'


##############
## save to disk one day ad a time
#############
def save_to_file(json_data,start_date):
	path="/tmp/facebook_marketing_api_"+start_date+".json"
	text_file = open(path, "w")
	n = text_file.write(json_data)
	text_file.close()
	print("file saved: "+path)


#############
## parse_Arg
###############
def parse_argv(argv):
    k1 = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["start_date="])
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (usage)
            sys.exit(0)
        elif opt in ("--start_date"):
           	print ("start_date found")
		k1=arg
    return k1

def main(argv):
	k1=parse_argv(argv)
	start_date=k1
    	print (start_date)


	########################
	## build output here
	########################
	fields =  ['campaign_id', 'impressions', 'spend','unique_inline_link_clicks']	
	params = {
  	'time_range' : {'since':str(start_date),'until':str(start_date)},
  	'breakdowns': ['country'],
  	'level':'campaign'
	#  'time_increment': 1	
	}


	#api calls 
	output_json=''	
	for ad in AdSet(ad_account_id).get_insights(fields=fields,params=params):
                data=str(ad).replace('<AdsInsights> ','')
                # remove newlline in json, add after end of line
                output_json=output_json+ ( data.replace("\n",' ') )+ "\n"

        # save response to disk
        save_to_file(output_json,start_date)


#######################
## main logic
##########################
if __name__ == "__main__":
	
    	#validate 1 arguments, the first is filename_arg+ 1x(kel,val)  = 3
    	if(len(sys.argv)==3):
        	main(sys.argv[1:])
    	else:
        	print "Error in arguments, try : "+(usage)
