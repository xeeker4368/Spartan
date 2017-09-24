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



}
<!--
ul {
    list-style-type: none;
    margin: 0;
    padding: 7px;
    width: 12%;
    background-color: #FF8800;
    position: fixed;
    height: 100%;
    overflow: auto;
}

li a {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
}

li a.active {
    background-color: #4CAF50;
    color: white;
}

li a:hover:not(.active) {
    background-color: #555;
    color: white;
}



</div>
    <div class="row">
        <div class="col-5";><p>
            <p class="wrap">
                <div class="scroll">
    <b>Virus Total Results:</b><br>
    <b>Total number of results: {{ VT_number_of_responses }}</b><br>
    {% for VT_responses in range(VT_number_of_responses) %}
    <br>
    <b>Scan date:</b> {{ VT_Response_Scan_Date[VT_responses] }}<br>
    <b>URL resolution:</b> {{ VT_Response_URL[VT_responses] }}<br>
    {% endfor %}
<script>
window.onscroll = function() {scrollFunction()};
</script>

                </div>
            </p>
        </div>
    </div>
<script>
window.onscroll = function() {scrollFunction()};
</script>
</div>
</div>
<form action="/" method="get"><input type="submit" value="Search again" button type="button" class="btn btn-primary"></form>

</body>
{% endblock %}