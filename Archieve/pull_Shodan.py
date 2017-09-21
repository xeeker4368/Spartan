"""
def pull_Shodan():
    global Shodan_Port_Count, Shodan_host, Shodan_Info, Shodan_Ports_Open, Shodan_Country, \
    Shodan_Host_Info, Shodan_Host_Info, shodan_host, Shodan_info, Shodan_Port, Shodan_Port_Count
    try:
        Shodan_Ports_Open = []
        Shodan_Port_Count = 0
        Shodan_Host_Info = ""
        shodan_host = ""
        Shodan_info = ""
        Shodan_Port = ""
        Shodan_Country = ""
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
    except Exception as e:
        return 'Error occurred : ' + str(e)
"""




#    return render_template('results.html', IP=request.form['Searchable_IP'],
#    Blacklist=(blacklist_site_name), number_of_sites=(site_count), \
#    shodan_host = (Shodan_host),Shodan_info = (Shodan_Info), Shodan_Port = (Shodan_Ports_Open), \
#    Shodan_Port_Count = (Shodan_Port_Count), Shodan_Country=(Shodan_Country), OTX = (OTX_Match_Found), \
#    Alexa = (Alexa_Match_Found))

#    Shodan_host = ""
#    Shodan_Info = ""
#    Shodan_Ports_Open = ""
#    Shodan_Port_Count = 0
#    Shodan_Country = ""