from tableausdk import *
from tableausdk.HyperExtract import *
import tableauserverclient as TSC
user='omid'
password='123'
tableau_auth = TSC.TableauAuth(user, password)
server = TSC.Server('http://10.1.0.1')
server.version = '3.6'
resource_id= 6109
with server.auth.sign_in(tableau_auth):
        print('connection made')
        print(server.version)
        #resource = server.workbooks.get_by_id(resource_id)
        server.workbooks.refresh(workbook_id='37A13D3E-64D9-4F9B-ACD5-2FCB0291BF24')
server.auth.sign_out()
print('connection closed')
