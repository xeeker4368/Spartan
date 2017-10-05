#!flask/bin/python
import re
import time
import urllib2
from StringIO import StringIO
from zipfile import ZipFile
from flask import request, render_template
from geoip import geolite2
import json
from app import app
from urllib2 import urlopen
import urllib
from configparser import ConfigParser

IP_Loc_File_Name = ""
IP_Loc_Domain = ""

Import_Date = time.strftime("%I:%M:%S")

#regex for matching IP's
IP_Regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"

#Read config.ini file from Config folder and assign to variables
parser = ConfigParser()
parser.read('config/config.ini')

#VirusTotal API
VT_API = parser.get('API', 'Virustotal_API')

#Shodan_API
Shodan_API = parser.get('API', 'Shodan_API')


#Main site
@app.route('/')
def root():
    return render_template('index.html')

#used to add a new site to the site file
@app.route('/add_site', methods=['POST', 'GET'])
def Add_Site():
    global Site_file
    return render_template('add_site.html')

#used to show the results of the 'add_site'
@app.route('/add_site_results', methods=['POST'])
def Add_Site_Results():
    global URL_List, content
    content = ""
    URL_List = "/home/localadmin/Documents/IP_List.txt"
    with open(URL_List, "a") as Site_file:
        Site_file.write(request.form['Additional_Site'])
        Site_file.write("\n")
    with open(URL_List) as URLS:
        content = URLS.readlines()
    Site_file.close()
    URLS.close()
    return render_template('add_site_results.html', Site_file=content)

#compiles and pulls all of the results from the various searches and publishes them to the results site.
@app.route('/results', methods=['POST', 'GET'])
def User_Input():
        pull_blacklist()
        pull_alexa()
        pull_OTX()
        pull_GeoIP()
        pull_cymon()
        pull_virustotal()
        site_count = len(blacklist_site_name)
        return render_template('results.html', IP=request.form['Searchable_IP'],
        Blacklist=(blacklist_site_name), number_of_sites=(site_count), \
        OTX = (OTX_Match_Found), Alexa = (Alexa_Match_Found), Geo_Country=(Geo_Country), Geo_City=(Geo_City), Geo_State=(Geo_State),  \
        Geo_Timezeone=(Geo_Timezeone), cymon_response_length=(cymon_response_length), cymon_title=(cymon_title), cymon_reported_by=(cymon_reported_by), \
        cymon_hostname=(cymon_hostname), cymon_tag=(cymon_tag), cymon_timestamp=(cymon_timestamp), VT_number_of_responses=(VT_number_of_responses), URL_Positive_Hits=(URL_Positive_Hits), \
        URL_Scan_Date=(URL_Scan_Date), VT_URL=(VT_URL), VT_URL_Resolutions=(VT_URL_Resolutions), \
        VT_Hostname=(VT_Hostname), VT_Last_Resolution=(VT_Last_Resolution),VT_number_of_URL_responses=(VT_number_of_URL_responses))

@app.route('/URL_results', methods=['POST', 'GET'])
def URL_Search():
    print "This is a URL"
    return

def download_unzip(input_zip):
    url = urllib2.urlopen(input_zip)
    unzipped_string = ''
    zipfile = ZipFile(StringIO(url.read()))
    for name in zipfile.namelist():
        unzipped_string += zipfile.open(name).read()
    return unzipped_string

# download something
def download_list(url):
    response = urllib2.urlopen(url)
    return response.read()


# searches a local text file (/home/localadmin/Documents/IP_List.txt) and matches it to a regex
def pull_blacklist():
    global site_number,blacklist_site_name, site_count
    try:
        blacklist_site_name = {}
        site_count = 0
        website_list = open('/home/localadmin/Documents/IP_List.txt')
        Blacklisted_pull_sites = website_list.readlines()
        file_length = len(Blacklisted_pull_sites)
        site_number = 0
        file_length = file_length - 1
        IP_Regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
        for site_number in range(0, file_length):
            for lines in urllib2.urlopen(Blacklisted_pull_sites[site_number]):
                (Blacklisted_pull_sites[site_number]) = (Blacklisted_pull_sites[site_number]).replace("\n", "")
                Searchable_IP = request.form['Searchable_IP']
                Searchable_IP = str(Searchable_IP).replace('u',"")
                lines = lines.replace("\n", "")
                lines = lines.replace("\r", "")
                IP_Match = re.findall(IP_Regex, lines)
                if IP_Match:
                    if  Searchable_IP == IP_Match[0]:
                        blacklist_site_name[site_count] = str(Blacklisted_pull_sites[site_number])
                        site_count = site_count + 1
                        continue
                else:
                        continue
    except:
        return

#pulls GEOIP info on the entered IP
def pull_GeoIP():
    try:
        global Geo_Country, Geo_City, Geo_State, Geo_Timezeone
        Geo_Country = ""
        Geo_City = ""
        Geo_State = ""
        Geo_Timezeone = ""
        Geo_IP_Info = geolite2.lookup(request.form['Searchable_IP'])
        Geo_Country = Geo_IP_Info.country
        Geo_City = Geo_IP_Info._data[u'city'][u'names'][u'en']
        Geo_State = Geo_IP_Info._data[u'subdivisions'][0][u'iso_code']
        Geo_Timezeone = Geo_IP_Info.timezone
        return
    except:
        return


def pull_OTX():
    global OTX_Match_Found
    OTX_Match_Found = ""
    OTX_url = ("https://reputation.alienvault.com/reputation.unix")
    otx_ip_list = download_list(OTX_url)
    otx_ip_list = otx_ip_list.split("\n")
    for OTX_IP in otx_ip_list:
        IP_Match = re.findall(IP_Regex, OTX_IP)
        if IP_Match:
            if IP_Match == request.form['Searchable_IP']:
                OTX_Match_Found = "OTX"
            continue
        else:
            continue

def pull_alexa():
    global Alexa_Match_Found
    Alexa_Match_Found = ""
    url = ("http://s3.amazonaws.com/alexa-static/top-1m.csv.zip")
    alexa_domains = download_unzip(url)
    hostfile = alexa_domains.split("\n")
    for alexa_hosts in hostfile:
        alexa_hosts = alexa_hosts.rstrip()
        IP_Match = re.findall(IP_Regex, alexa_hosts)
        if IP_Match:
            if IP_Match == request.form['Searchable_IP']:
                Alexa_Match_Found = "Alexa"
                continue
            else:
                continue

def pull_cymon():
    global cymon_response_length, cymon_title, cymon_reported_by, cymon_hostname, cymon_tag, cymon_timestamp
    cymon_response_length, cymon_title, cymon_reported_by, cymon_hostname, cymon_tag, cymon_timestamp = {}, {}, {}, {}, {}, {}
    cymon_IP_request = 'https://api.cymon.io/v2/ioc/search/ip/' + (request.form['Searchable_IP']) + '?size=3'
    cymon_response_ip = json.load(urlopen(cymon_IP_request))
    cymon_response_length = cymon_response_ip[u'hits'].__len__()
    if cymon_response_ip[u'hits'].__len__() == 0:
        cymon_domain_legth = "No hits found"
    elif cymon_response_length < 10:
        cymon_response_length = cymon_response_ip[u'hits'].__len__()
    else:
        cymon_response_length == 10
    for cymon_responses in range(cymon_response_length):
        cymon_title[cymon_responses] = cymon_response_ip[u'hits'][cymon_responses].get(u'title')
        cymon_reported_by[cymon_responses] = cymon_response_ip[u'hits'][cymon_responses].get(u'reported_by')
        cymon_hostname[cymon_responses] = cymon_response_ip[u'hits'][cymon_responses][u'ioc'].get(u'hostname')
        cymon_tag[cymon_responses] = str(cymon_response_ip[u'hits'][cymon_responses].get(u'tags'))
        cymon_timestamp = cymon_response_ip[u'hits'][cymon_responses].get(u'timestamp')




def pull_virustotal():
    global VT_number_of_responses, URL_Positive_Hits, URL_Scan_Date, VT_URL, VT_URL_Resolutions, \
        VT_URL_Resolutions, VT_Hostname, VT_Last_Resolution, VT_number_of_URL_responses
    VT_number_of_responses, URL_Positive_Hits, URL_Scan_Date, VT_URL, VT_URL_Resolutions, \
    VT_URL_Resolutions, VT_Hostname, VT_Last_Resolution = {}, {}, {}, {}, {}, {}, {}, {}
    VT_url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    VT_parameters = {'ip': request.form['Searchable_IP'], 'apikey': VT_API}
    VT_response = urllib.urlopen('%s?%s' % (VT_url, urllib.urlencode(VT_parameters))).read()
    VT_response_dict = json.loads(VT_response)
    VT_number_of_URL_responses = VT_response_dict[u'resolutions'].__len__()
    try:
        if  VT_response_dict[u'detected_urls'].__len__() == 0:
            VT_URL[0] = "No flagged URL's Found"
        elif VT_number_of_URL_responses < 10:
            VT_number_of_URL_responses = VT_response_dict[u'resolutions'].__len__()
        else:
            VT_number_of_URL_responses = 10
        for URL_Responses in range(VT_number_of_URL_responses):
            VT_URL[URL_Responses] = VT_response_dict[u'detected_urls'][URL_Responses].get(u'url', 'None')
            URL_Positive_Hits[URL_Responses] = VT_response_dict[u'detected_urls'][URL_Responses].get(u'positives')
            URL_Scan_Date[URL_Responses] = VT_response_dict[u'detected_urls'][URL_Responses].get(u'scan_date')
    except:
        VT_number_of_URL_responses = 0

    VT_URL_Resolutions = VT_response_dict[u'resolutions'].__len__()
    if VT_response_dict[u'resolutions'].__len__() == 0:
        VT_Hostname = "No Hostnames found"
        return
    elif VT_URL_Resolutions < 10:
        VT_URL_Resolutions = VT_response_dict[u'resolutions'].__len__()
    else:
        VT_URL_Resolutions = 10
    for VT_URLs in range(VT_URL_Resolutions):
            VT_Hostname[VT_URLs] = VT_response_dict[u'resolutions'][VT_URLs].get(u'hostname')
            VT_Last_Resolution[VT_URLs] = VT_response_dict[u'resolutions'][VT_URLs].get(u'last_resolved')

app.run(debug='true')
#app.run(host='0.0.0.0', port=80, threaded=True)
