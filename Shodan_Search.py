import shodan
IP = raw_input("Enter IP ")

ShodanHost = ""
ShodanIP = ""
Shodan_api = shodan.Shodan("U2II0MBVysVVrziUhEi7LnFxQvNcbCVV")
Shodan_Host_Info = Shodan_api.host(IP)
#    print """Hostname: %s
#Organization: %s
#IP: %s \
#            """ % (Shodan_Host_Info['hostnames'], Shodan_Host_Info.get('org', 'n/a'), \
#           Shodan_Host_Info.get('ip_str', 'n/a'))
#    for Shodan_Port in Shodan_Host_Info['data']:
#        print """Open Ports: %s""" % (Shodan_Port['port'])
ShodanHost = Shodan_Host_Info['hostnames']
ShodanIP = Shodan_Host_Info.get('ip_str', 'n/a')