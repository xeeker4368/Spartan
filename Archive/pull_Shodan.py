# See also
#
#  * http://securityintelligence.com/a-gentle-introduction-to-the-x-force-exchange-api
#  * https://api.xforce.ibmcloud.com/doc/#!/Authentication/get_auth_api_key
#
import requests
import json

URL = 'https://xforce-api.mybluemix.net:443'

# Get an anonymus token
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US',
}
r = requests.get(URL + '/auth/anonymousToken', headers=headers)
token = json.loads(r._content)['token']
headers['Authorization'] = 'Bearer %s' % token

# Query
r = requests.get(URL + '/vulnerabilities', headers=headers)
json.loads(r._content)