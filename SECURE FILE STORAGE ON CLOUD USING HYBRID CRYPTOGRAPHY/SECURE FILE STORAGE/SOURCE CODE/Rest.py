import requests
import json
base = 'https://firstproject-bd0f1-default-rtdb.firebaseio.com/'
class Rest:
    def post(self,url,data):
        resturl = base+url+'.json'
        r = requests.post(resturl, data)
        return json.loads(r.text)
    
    def get(self,url):
        resturl = base+url+'.json'
        r = requests.get(resturl)
        return json.loads(r.text)
    
    
    def delete(self,url):
        resturl = base+url+'.json'
        r = requests.delete(resturl)
        return json.loads(r.text)
    
    
    def put(self,url,data):
        resturl = base+url+'.json'
        print(resturl)
        r = requests.put(resturl, data)
        return json.loads(r.text)

    def load(self,url):
        resturl = base+url+'.json'
        r = requests.get(resturl)
        return json.loads(r.text)
