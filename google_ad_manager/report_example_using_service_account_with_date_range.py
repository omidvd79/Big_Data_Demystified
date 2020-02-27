#!/usr/bin/env python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Initializes a AdManagerClient using a Service Account."""

import sys, getopt

from datetime import datetime
from datetime import timedelta

from googleads import ad_manager
from googleads import oauth2
from googleads import errors
import tempfile


# OAuth2 credential information. In a real application, you'd probably be
# pulling these values from a credential storage.
KEY_FILE = '/home/omid/my_gcp_private_key_service_account.json'

# Ad Manager API information.
APPLICATION_NAME = 'jutomate'
NETWORK_CODE='6690'

def report(key_file, application_name,startDate,endDate):
  oauth2_client = oauth2.GoogleServiceAccountClient(
      key_file, oauth2.GetAPIScope('ad_manager'))

  client = ad_manager.AdManagerClient(
      oauth2_client, application_name, NETWORK_CODE)

  #networks = ad_manager_client.GetService('NetworkService').getAllNetworks()
  #for network in networks:
  #  print('Network with network code "%s" and display name "%s" was found.'
  #        % (network['networkCode'], network['displayName']))

  # Initialize a DataDownloader.
  report_downloader = client.GetDataDownloader(version='v201911')
  # Set the start and end dates of the report to run (past 0 days, you can change to what u need).
  end_date = datetime.strptime( startDate, "%Y-%m-%d").date()
  
  start_date = datetime.strptime( endDate, "%Y-%m-%d").date()
  
  print ('start_date: ', start_date)
  print ('end_date: ', end_date)
  
  report_filename_prefix='report_example_using_service_account_with_date_range'
  
 # Create report job.
  report_job = {
      'reportQuery': {
          'dimensions': ['DATE', 'AD_UNIT_NAME'],
          'adUnitView': 'HIERARCHICAL',
          'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                      'ADSENSE_LINE_ITEM_LEVEL_IMPRESSIONS',
                      'ADSENSE_LINE_ITEM_LEVEL_CLICKS',
                      'TOTAL_LINE_ITEM_LEVEL_IMPRESSIONS',
                      'TOTAL_LINE_ITEM_LEVEL_CPM_AND_CPC_REVENUE'],
          'dateRangeType': 'CUSTOM_DATE',
          'startDate': start_date,
          'endDate': end_date
      }
  }


  try:
    # Run the report and wait for it to finish.
    report_job_id = report_downloader.WaitForReport(report_job)
  except errors.AdManagerReportError as e:
    print('Failed to generate report. Error was: %s' % e)
 
 # Change to your preferred export format.
  export_format = 'CSV_DUMP'

  report_file = tempfile.NamedTemporaryFile(suffix='_'+report_filename_prefix+'_'+startDate+'__'+endDate+'.csv.gz', delete=False)

  # Download report data.
  report_downloader.DownloadReportToFile(
      report_job_id, export_format, report_file)

  report_file.close()
  
    # Display results.
  print('Report job with id "%s" downloaded to:\n%s' % (
      report_job_id, report_file.name))

def main(argv):
   startDate = ''
   endDate = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["start=","end="])
   except getopt.GetoptError:
      print ('example_python_command_line_arguments.py -s <startDate> -e <endDate>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('example_python_command_line_arguments.py -s <startDate> -e <endDate>')
         sys.exit()
      elif opt in ("-s", "--start"):
         startDate = arg
      elif opt in ("-e", "--end"):
         endDate = arg
   print ('start date is ', startDate)
   print ('end   date is ', endDate)
   report(KEY_FILE, APPLICATION_NAME,startDate,endDate)
   
if __name__ == '__main__':
  main(sys.argv[1:])
