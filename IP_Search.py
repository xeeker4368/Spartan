import re
import urllib2
import time
from zipfile import ZipFile
from StringIO import StringIO
from tkinter import *
import webbrowser
import shodan
from flask import request,render_template
from app import app

global Blacklisted_pull_sites
global Searchable_IP

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/results', methods = ['POST','GET'])
def results():
    sites_from_txt()

    Searchable_IP = request.form['Searchable_IP']
    return render_template('results.html', IP=Searchable_IP, Blacklist=(sites_from_txt.Blacklisted_pull_sites[site_number]))


app.run(debug = True)

def url_open_XForce():
    IBM_XForce = "https://exchange.xforce.ibmcloud.com/ip/" + results.Searchable_IP
    webbrowser.open_new_tab(IBM_XForce)


def url_open_Abuse_IP():
    Abuse_IP_DB = "https://www.abuseipdb.com/check/" + results.Searchable_IP
    webbrowser.open_new_tab(Abuse_IP_DB)


def url_open_Whois():
    Whois_website = "http://whois.domaintools.com/" + results.Searchable_IP
    webbrowser.open_new_tab(Whois_website)

# IP Match Regex
site_number = 0
IP_Regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"

#5.196.1.129

IP_Loc_File_Name = ""
IP_Loc_Domain = ""

Import_Date = time.strftime("%I:%M:%S")

website_list = open('/home/localadmin/Documents/IP_List.txt')
Blacklisted_pull_sites = website_list.readlines()
file_length = len(Blacklisted_pull_sites)


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

# pulls the alexa top 1 million
def pull_alexa():
    url = ("http://s3.amazonaws.com/alexa-static/top-1m.csv.zip")
    domains = download_unzip(url)
    hostfile = domains.split("\n")
    for hosts in hostfile:
        hosts = hosts.rstrip()
        IP_Match = re.findall(IP_Regex, hosts)
        if IP_Match:
            if IP_Match == results.Searchable_IP:
                print(("%s found!" % (hosts)))
                continue
            else:
                continue

# get associated otx list
def pull_OTX():
    OTX_Match_Found = ""
    OTX_url = ("https://reputation.alienvault.com/reputation.unix")
    otx_ip_list = download_list(OTX_url)
    otx_ip_list = otx_ip_list.split("\n")
    for OTX_IP in otx_ip_list:
        IP_Match = re.findall(IP_Regex, OTX_IP)
        if IP_Match:
            if IP_Match[0] == results.Searchable_IP:
                print results.Searchable_IP, "Found in OTX"
                OTX_Match_Found = results.Searchable_IP
            continue
        else:
            continue

def pull_Shodan():
    ShodanHost = ""
    ShodanIP = ""
    Shodan_api = shodan.Shodan("U2II0MBVysVVrziUhEi7LnFxQvNcbCVV")
    Shodan_Host_Info = Shodan_api.host(results.Searchable_IP)
#    print """Hostname: %s
#Organization: %s
#IP: %s \
#            """ % (Shodan_Host_Info['hostnames'], Shodan_Host_Info.get('org', 'n/a'), \
#           Shodan_Host_Info.get('ip_str', 'n/a'))
#    for Shodan_Port in Shodan_Host_Info['data']:
#        print """Open Ports: %s""" % (Shodan_Port['port'])
#    ShodanHost == (Shodan_Host_Info['hostnames'])
#    ShodanIP == Shodan_Host_Info.get('ip_str', 'n/a')


def sites_from_txt():
    for site_number in range(0,file_length):
        for lines in urllib2.urlopen(Blacklisted_pull_sites[site_number]):
            lines = lines.replace("\n", "")
            lines = lines.replace("\r", "")
            IP_Match = re.match(IP_Regex, lines)
            if IP_Match:
                if results.Searchable_IP == lines:
                    print results.Searchable_IP , " found on the %s" %(Blacklisted_pull_sites[site_number])
                    continue
            else:
                continue

pull_OTX()
pull_Shodan()
pull_alexa()
