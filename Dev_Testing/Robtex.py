import urllib
import json


Searchable_IP = '90.156.201.27'

VT_url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
VT_parameters = {'ip': Searchable_IP, 'apikey': '40dc8379e9077009a2315e0a883b65d01c8e1e66002b55f732540845c83570ae'}
VT_response = urllib.urlopen('%s?%s' % (VT_url, urllib.urlencode(VT_parameters))).read()
VT_response_dict = json.loads(VT_response)
VT_number_of_responses = VT_response_dict[u'detected_urls'].__len__()
print VT_response_dict[u'as_owner']
print VT_response_dict[u'country']
for VT_responses in range(VT_number_of_responses):
    VT_Response_Scan_Date = VT_response_dict[u'detected_urls'][VT_responses][u'scan_date']
    VT_Response_URL = VT_response_dict[u'detected_urls'][VT_responses][u'url']
    VT_Response_Positives = VT_response_dict[u'detected_urls'][VT_responses][u'positives']

    print "Positives:" + str(VT_Response_Positives)
    print "Scan Date: " + VT_Response_Scan_Date
    print "Scanned URL Resolution: " + VT_Response_URL

VT_number_of_resolution = VT_response_dict[u'resolutions'].__len__()
TV_total_Domain_resolution = VT_response_dict[u'resolutions']
print "Number of resolutions: %s" % (VT_number_of_resolution)

for VT_Resolutions in range(VT_number_of_resolution):
    VT_Resolutions_Hostnames = TV_total_Domain_resolution[VT_Resolutions][u'hostname']
    VT_Resolutions_Last_Resolution = TV_total_Domain_resolution[VT_Resolutions][u'last_resolved']
    print "Last resolved: %s %s " % (VT_Resolutions_Hostnames, VT_Resolutions_Last_Resolution)