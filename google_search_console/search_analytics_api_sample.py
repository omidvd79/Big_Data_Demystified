from __future__ import print_function

import argparse
import sys
from googleapiclient import sample_tools

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))


def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')

  request = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['country', 'device','page','query'],
  }
  response = execute_request(service, flags.property_uri, request)
  write_reponse_to_file(response,flags.start_date,flags.end_date)

  #print_table(response, 'Group by country ,device,page,query')

  # Group by total number of Search Appearance count.
  # Note: It is not possible to use searchAppearance with other
  # dimensions.
  #request = {
  #    'startDate': flags.start_date,
  #    'endDate': flags.end_date,
  #    'dimensions': ['searchAppearance'],
  #    'rowLimit': 10
  #}
  #response = execute_request(service, flags.property_uri, request)
  #print_table(response, 'Search Appearance Features')

def execute_request(service, property_uri, request):
  """Executes a searchAnalytics.query request.
  Args:
    service: The webmasters service to use when executing the query.
    property_uri: The site or app URI to request data for.
    request: The request to be executed.
  Returns:
    An array of response rows.
  """
  return service.searchanalytics().query(
      siteUrl=property_uri, body=request).execute()


def save_table(response):
  text='country,device,page,query,clicks,impressions,ctr,position'+'\n'
  if 'rows' not in response:
    return text

  rows = response['rows']
  for row in rows:
  	metrics=str(row['clicks'])+","+str(row['impressions'])+","+ str(row['ctr'])+","+ str(row['position'])
	for key in row['keys']:
		text=text+key.encode('utf-8').strip()+","
	text=text+metrics+"\n"
	
  return text



def write_reponse_to_file(response,start_date,end_date):
	
	file = open("/tmp/search_console_"+start_date+"__"+end_date+".csv", "w")
	file.write(save_table(response))
	file.close()

if __name__ == '__main__':
  main(sys.argv)
