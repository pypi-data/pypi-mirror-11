import urllib3, urllib
import json
from paralleldots.config import get_api_key
http = urllib3.PoolManager()
def get_taxonomy(s1):
	apikey  = get_api_key()
	if not apikey == None:
		params = { 'sentence1' : s1, 'apikey' : apikey}
		en_params = urllib.urlencode(params)
		url = 'http://apis.paralleldots.com/taxonomy?'+en_params
		r =  http.request('GET',url)
		return json.loads(r.data)
	else:
		return "API key does not exist"




