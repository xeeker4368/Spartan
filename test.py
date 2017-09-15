#!flask/bin/python
from flask import request, redirect, Flask, render_template
from app import app
import urllib2
import time
import re
import shodan
import webbrowser
from zipfile import ZipFile
from StringIO import StringIO

IP_Loc_File_Name = ""
IP_Loc_Domain = ""

Import_Date = time.strftime("%I:%M:%S")

# unzip something
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

IP_Regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/results', methods=['POST', 'GET'])
def Actions_to_IP():
    pull_blacklist()
    pull_alexa()
    pull_OTX()
    if pull_Shodan() == "{NameError}name 'Shodan_api' is not defined:":
        return
    else:
        site_count = len(blacklist_site_name)
    return render_template('results.html', IP=request.form['Searchable_IP'],
    Blacklist=(blacklist_site_name), number_of_sites=(site_count), \
    shodan_host = (Shodan_host),Shodan_info = (Shodan_Info), Shodan_Port = (Shodan_Ports_Open), \
    Shodan_Port_Count = (Shodan_Port_Count), Shodan_Country=(Shodan_Country), OTX = (OTX_Match_Found), \
    Alexa = (Alexa_Match_Found))

def pull_blacklist():
    global site_number,blacklist_site_name, site_count
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
            IP_Match = re.match(IP_Regex, lines)
            if IP_Match:
                if  Searchable_IP == lines:
                    blacklist_site_name[site_count] = str(Blacklisted_pull_sites[site_number])
                    site_count = site_count + 1

                    continue
            else:
                continue

def pull_Shodan():
    global Shodan_Port_Count, Shodan_host, Shodan_Info, Shodan_Ports_Open, Shodan_Country, Shodan_Host_Info
    Shodan_Ports_Open = []
    Shodan_Port_Count = 0
    Shodan_Host_Info = ""
    Requested_IP = request.form['Searchable_IP']
    Requested_IP = str(Requested_IP).replace('u',"")
    Shodan_api = shodan.Shodan("U2II0MBVysVVrziUhEi7LnFxQvNcbCVV")
    print Shodan_api
    Shodan_Host_Info = Shodan_api.host(Requested_IP)
    Shodan_host = str(Shodan_Host_Info['hostnames'])
    Shodan_Country = str(Shodan_Host_Info['country_name'])
    Shodan_host = str(Shodan_host).replace('u',"")
    Shodan_Info = Shodan_Host_Info.get('org', 'n/a')
    for Shodan_Port in Shodan_Host_Info['data']:
        Shodan_Ports_Open.append(Shodan_Port['port'])
        Shodan_Port_Count = len(Shodan_Ports_Open)


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

app.run(debug = True)
