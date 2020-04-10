'''
import google as g
data = g.doGoogleSearch('the martian')
print data.results
'''
'''
from pygoogle import pygoogle
g = pygoogle('the martian')
g.pages = 5
print '*Found %s results*'%(g.get_result_count())
g.get_urls()
'''

import pprint

from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyDRRpR3GS1F1_jKNNM9HCNd2wJQyPG3oN0")

  res = service.cse().list(
      q='lectures',
      #cx='017576662512468239146:omuauf_lfve',
    ).execute()
  pprint.pprint(res)

if __name__ == '__main__':
  main()