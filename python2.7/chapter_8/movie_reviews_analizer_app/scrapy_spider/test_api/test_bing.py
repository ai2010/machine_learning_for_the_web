import urllib
import urllib2
import requests
import json
from requests.auth import HTTPBasicAuth
import os.path as o_p

#############################################################
'''
Registration steps:
1. register online on https://datamarket.azure.com
2. in my account take the 'Primary Account Key'
3. register a new application: (under Developers->Register; put Redirect URI: https://www.bing.com) (WITHOUT THAT IT WILL NOT WORK!!!!!!!!!!!)


'''
###############################################################
# Bing API key
API_KEY = "X/+6jgJS0FkPGql4w7tphwJh2dj+trSqXxcnbSZUHPc"
 
def bing_api(query, source_type = "Web", top = 10, format = 'json'):
    keyBing = API_KEY        # get Bing key from: https://datamarket.azure.com/account/keys
    credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
    searchString = '%27X'+query.replace(" ",'+')+'movie+review%27'
    #max allowed is 50
    top = 50
    offset = 0

    url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
          'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

    #url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
    #      'Query=%s&$format=json' % (searchString)
    
    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request) 

    results = json.load(response)
    #file_test = open('bing_the_martian_results.json','w')
    #file_test.write(json.dumps(results))
    
    return results
    
def parse_bing_results():
    file_data = open(o_p.dirname(o_p.abspath(__file__))+'/bing_the_martian_results.json','r')
    bing_json = json.load(file_data)
    print len(bing_json['d']['results'])
    reviews_urls = [ d['Url'] for d in bing_json['d']['results']]
    print reviews_urls
    
    
results =  bing_api('vacation')
print results
print len(results['d']['results'])
#parse_bing_results()