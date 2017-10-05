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

IP_Loc_File_Name = ""
IP_Loc_Domain = ""

Import_Date = time.strftime("%I:%M:%S")

#regex for matching IP's
IP_Regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"

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
    global URL_List
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
        site_count = len(blacklist_site_name)
        return render_template('results.html', IP=request.form['Searchable_IP'],
        Blacklist=(blacklist_site_name), number_of_sites=(site_count), \
        OTX = (OTX_Match_Found), \
        Alexa = (Alexa_Match_Found), Geo_Country=(Geo_Country), Geo_Subvisions=(Geo_Subvisions), \
        Geo_Timezeone=(Geo_Timezeone), cymon_title=(cymon_response_title), cymon_feed=(cymon_response_feed), \
        cymon_time = (cymon_response_time), cymon_ioc_url=(cymon_response_ioc_url), \
        cymon_ioc_ip =(cymon_response_ioc_ip), cymon_legth=(cymon_response_leght))


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
    global Geo_Country, Geo_Subvisions, Geo_Timezeone
    Geo_IP_Info = geolite2.lookup(request.form['Searchable_IP'])
    Geo_Country = Geo_IP_Info.country
    Geo_Subvisions = Geo_IP_Info.subdivisions
    Geo_Timezeone = Geo_IP_Info.timezone


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
    global cymon_response_title, cymon_response_feed, \
    cymon_response_time, cymon_response_ioc, cymon_response_ioc_ip, cymon_response_ioc_url, cymon_response_leght
    cymon_request = 'https://api.cymon.io/v2/ioc/search/ip/' + request.form['Searchable_IP']
    cymon_response_title = {}
    cymon_response_feed = {}
    cymon_response_time = {}
    cymon_response_ioc = {}
    cymon_response_ioc_ip = {}
    cymon_response_ioc_url = {}
    cymon_response_body = json.load(urlopen(cymon_request))
    cymon_response_leght = cymon_response_body[u'total']
    for cymon_legth in range(cymon_response_leght):
        cymon_response_title[cymon_legth] = cymon_response_body[u'hits'][cymon_legth].get(u'title')
        cymon_response_feed[cymon_legth] = cymon_response_body[u'hits'][cymon_legth].get(u'feed')
        cymon_response_time[cymon_legth] = cymon_response_body[u'hits'][cymon_legth].get(u'timestamp')
        cymon_response_ioc[cymon_legth] = cymon_response_body[u'hits'][cymon_legth].get(u'ioc')
        cymon_response_ioc_ip[cymon_legth] = cymon_response_ioc[cymon_legth].get(u'ip')
        cymon_response_ioc_url[cymon_legth] = cymon_response_ioc[cymon_legth].get(u'url')
        cymon_legth = cymon_legth + 1


app.run(debug='true')
#app.run(host='0.0.0.0', port=80)