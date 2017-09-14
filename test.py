#!flask/bin/python
from flask import request, redirect, Flask, render_template
from app import app
import urllib2
import time
import re
import shodan
import webbrowser

IP_Loc_File_Name = ""
IP_Loc_Domain = ""

Import_Date = time.strftime("%I:%M:%S")

#website_list = open('/home/localadmin/Documents/IP_List.txt')
#Blacklisted_pull_sites = website_list.readlines()
#file_length = len(Blacklisted_pull_sites)


IP_Regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"

@app.route('/')
def root():
    return render_template('index.html')


#@app.route('/results', methods=['POST', 'GET'])
#def results():
#    global Searchable_IP
#    Searchable_IP = request.form['Searchable_IP']
#    Searchable_IP = Searchable_IP.replace("\u", "")
#    pull_binarybanlist()
#    return render_template('results.html', IP=Searchable_IP,
#    Blacklist=pull_binarybanlist())



@app.route('/results', methods=['POST', 'GET'])
def Actions_to_IP():
    pull_blacklist()
    pull_Shodan()
    site_count = len(blacklist_site_name)
    return render_template('results.html', IP=request.form['Searchable_IP'],
    Blacklist=(blacklist_site_name), number_of_sites=(site_count), \
    shodan_host = (Shodan_host),Shodan_info = (Shodan_Info), Shodan_Port = (Shodan_Ports_Open), \
    Shodan_Port_Count = (Shodan_Port_Count), Shodan_Country=(Shodan_Country))

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
    global Shodan_Port_Count, Shodan_host, Shodan_Info, Shodan_Ports_Open, Shodan_Country
    Shodan_Ports_Open = []
    Shodan_Port_Count = 0
    Requested_IP = request.form['Searchable_IP']
    Requested_IP = str(Requested_IP).replace('u',"")
    Shodan_api = shodan.Shodan("U2II0MBVysVVrziUhEi7LnFxQvNcbCVV")
    Shodan_Host_Info = Shodan_api.host(Requested_IP)
    Shodan_host = str(Shodan_Host_Info['hostnames'])
    Shodan_Country = str(Shodan_Host_Info['country_name'])
    Shodan_host = str(Shodan_host).replace('u',"")
    Shodan_Info = Shodan_Host_Info.get('org', 'n/a')
    for Shodan_Port in Shodan_Host_Info['data']:
        Shodan_Ports_Open.append(Shodan_Port['port'])
    Shodan_Port_Count = len(Shodan_Ports_Open)


#webbrowser.open_new_tab("https://exchange.xforce.ibmcloud.com/ip/" + request.form['Searchable_IP']))
#    Abuse_IP_DB = webbrowser.open_new_tab("https://www.abuseipdb.com/check/" + request.form['Searchable_IP'])
#    Whois_website = webbrowser.open_new_tab("http://whois.domaintools.com/" + request.form['Searchable_IP'])
#    return IBM_XForce, Abuse_IP_DB, Whois_website
app.run(debug = True)

#        Requested_IP = request.form['Searchable_IP']
#        Shodan_api = shodan.Shodan("U2II0MBVysVVrziUhEi7LnFxQvNcbCVV")
#        Shodan_Host_Info = Shodan_api.host(Requested_IP)
#        Shodan_host = Shodan_Host_Info['hostnames']