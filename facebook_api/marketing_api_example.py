from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi


access_token = 'token'
app_secret = 'secret'
ad_account_id = 'act_123456'
api = FacebookAdsApi.init(access_token=access_token,app_secret=app_secret)
output_json=''
start_date='1970-01-01'

########################
## build output here
########################
fields =  ['date_start', 'date_stop','campaign_id','campaign_name', 'ad_name', 'impressions', 'inline_link_clicks', 'spend']
params = {
  'export_columns':['CSV'],
  'time_range' : {'since':'2020-05-09','until':'2020-05-09'},
  'fields': [
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.ad_name,
        AdsInsights.Field.spend,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.buying_type,
        AdsInsights.Field.objective,        
        AdsInsights.Field.actions
      ], 
  'breakdown': ['country'],
  'level':'ad',
  'time_increment': 1
}


##############
## save to disk one day ad a time
#############
def save_to_file(json_data):
	path="/tmp/facebook_marketing_api_"+start_date+".json"
	text_file = open(path, "w")
	n = text_file.write(json_data)
	text_file.close()
	print("file saved: "+path)



#######################
## main logic
##########################

#api calls 
for ad in AdSet(ad_account_id).get_insights(fields=fields,params=params):
	data=str(ad).replace('<AdsInsights> ','')
	# remove newlline in json, add after end of line
	output_json=output_json+ ( data.replace("\n",' ') )+ "\n"

# save response to disk
save_to_file(output_json)
