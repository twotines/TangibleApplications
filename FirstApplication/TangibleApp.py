#!/usr/bin/python3

#"""Tangible app is just a simple application that makes a few call to the tangibleAPI and make a couple of request to the devices found"""
import sys
import httplib2
import urllib.parse
import json 

def printResponse(resp, content):
    print('from API headers: >>> ',resp)
    #    print('from API body: >> ',content.decode('utf-8'))
    try:
        jsonContent = json.loads(content.decode('utf-8'))
        print('from API body: >>> ', json.dumps(jsonContent, indent = 2))
        pass
    except ValueError:
        print('from API body: >>> ', content.decode('utf-8'))
        pass
    pass

def formatParams(params):
    return (json.dumps(params), urllib.parse.urlencode(params))

h = httplib2.Http(".cache")
baseURI = "http://localhost:9998/tangibleapi"

print()
print('asking a GET to: '+baseURI)
resp, content = h.request(baseURI, "GET")

printResponse(resp,content)
sys.stdin.readline()

print()
print( 'trying to register the application' )
params = {'appname':'myGreatTangibleApp', 'description':'a simple but soon-to-be-great application written in python' }
json_params, url_params = formatParams(params)

sys.stdin.readline()
print()
h = httplib2.Http(".cache")
print( 'request params >>> ',params) 
resp, content = h.request(baseURI+'/app/registration', "PUT", url_params, headers={'content-type':'application/json'} )
content_str = content.decode('utf-8')
msg_obj = json.loads(content_str)
appUUID = msg_obj['msg']
printResponse(resp, content)
print( 'from API >>> the freshly created appUUID is ', appUUID)

#let's keep appUUID for later : we will use it to quite the applicaiton
#and actually each call to the api requires to send it so ... we'll need it a lot...

sys.stdin.readline()
print()
h = httplib2.Http(".cache")
params = {}
json_params, url_params = formatParams(params)
#print("json_params : ", json_params)
resp, content = h.request(baseURI+'/'+appUUID+'/device', "GET")
printResponse(resp,content)


sys.stdin.readline()
print()
h = httplib2.Http(".cache")
msg_obj = json.loads(content.decode('utf-8'))
deviceId = msg_obj['msg'][2]['id']
#deviceId = 'myUniqueIdThatIsNotARealOneYet'
print("requesting the device: ", deviceId)
#print("json_params : ", json_params)
resp, content = h.request(baseURI+'/'+appUUID+'/device/reservation/'+deviceId, "PUT")
printResponse(resp,content)


sys.stdin.readline()
print()
while True:
    print("enter a valid color please")
    color = sys.stdin.readline().strip()
    if color == '' or color == 'quit':
        break
    h = httplib2.Http(".cache")
    params["color"] = color
    json_params, url_params = formatParams(params)
    #print('the current params are: '+json_params)
    print('the current params are: '+url_params)
    #resp, content = h.request(baseURI+'/'+appUUID+'/device_methods/'+deviceId+'/show_color/', "PUT", json_params)
    #printResponse(resp, content)
    #print()
    h = httplib2.Http(".cache")
    resp, content = h.request(baseURI+'/'+appUUID+'/device_methods/'+deviceId+'/show_color/', "PUT", url_params)
    printResponse(resp, content)
    pass

sys.stdin.readline()
print()
h = httplib2.Http(".cache")
#deviceId = 'myUniqueIdThatIsNotARealOneYet'
print("removing the reservation on the device: ", deviceId)
#print("json_params : ", json_params)
resp, content = h.request(baseURI+'/'+appUUID+'/device/reservation/'+deviceId, "DELETE")
printResponse(resp,content)
