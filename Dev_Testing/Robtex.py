import json
from urllib2 import urlopen

Searchable_IP = "63.247.140.224"


cymon_request = 'https://api.cymon.io/v2/ioc/search/ip/' + Searchable_IP
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



for legth in range(cymon_response_leght):
    print cymon_response_title[legth]
    print cymon_response_feed[legth]
    print cymon_response_time[legth]
    print cymon_response_ioc_ip[legth]
    print cymon_response_ioc_url[legth]
    print legth
    print



{% extends "base.html" %}

{% block content %}
<style>
.bs-example  div[class^="col"] {
	border: 1px solid white;
	background: #f5f5f5;
	text-align: center;
	padding-top: 8px;
	padding-bottom: 8px;
	}
