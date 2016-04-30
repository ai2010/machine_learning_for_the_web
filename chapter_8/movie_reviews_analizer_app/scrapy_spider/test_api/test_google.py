import requests
s = requests.Session()
s.params['key'] = 'AIzaSyCq7kpSt9xSv2WiUlD1F-8HyAuhxE0u104'
s.params['cx'] = '000520718210502444314:ykpllu5scrs'
result = s.get('https://www.googleapis.com/customsearch/v1', params={'q': 'the martian review'})
print result.text.encode('utf-8')