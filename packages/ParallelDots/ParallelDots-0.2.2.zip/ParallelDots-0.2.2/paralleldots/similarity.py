import urllib2, urllib
import json
from paralleldots.config import get_api_key

def get_similarity(s1,s2):
	apikey  = get_api_key()
	if not apikey == None:
		params = { 'sentence1' : s1, 'sentence2' : s2, 'apikey' : apikey}
		en_params = urllib.urlencode(params)
		url = 'http://apis.paralleldots.com/semanticsimilarity?'+en_params
		a =  urllib2.urlopen(url)
		return json.load(a)
	else:
		return "API key does not exist"


