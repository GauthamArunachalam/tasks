from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import requests
import threading

app = Flask(__name__)

#To return the base url for api call to be made to bing api
def getBaseURL(urlPathName):
    if urlPathName == "business":
        return "https://dev.virtualearth.net/REST/v1/LocalSearch"
    elif urlPathName == "isochrone":
        return "https://dev.virtualearth.net/REST/v1/Routes/Isochrones"
    elif urlPathName == "isochroneAsync":
        return "https://dev.virtualearth.net/REST/v1/Routes/IsochronesAsync"   
    elif urlPathName == "IsochronesAsyncCallback":
        return "https://dev.virtualearth.net/REST/v1/Routes/IsochronesAsyncCallback"     

#To return the bing API key  
def getBingKey():
    return "AkId5p0j6TMZ1rKjLKVSlxMwz74ZYpo_yN_4YOB0L_LXnYu-xhPIKnLNwYg0gexQ"

def getErrorResponse():
    errorJSON = '{"message" : "Unable to fetch data from bing api"}'
    return jsonify(errorJSON)

@app.route("/isochrone", methods=["GET"])
def isochrone():
    baseUrl = getBaseURL("isochrone")
    params = ["waypoint", "maxDistance", "distanceUnit", "optimize", "travelMode", "maxTime", "timeUnit", "dateTime"]
    queryString = ""

    for param in params:
        if param in request.args:
            queryString += param + "=" + request.args[param]+"&"

    queryString += "key=" + getBingKey()
    baseUrl = baseUrl + "?" + queryString

    try:
        response = requests.get(baseUrl)
        if response.status_code == 200:
            return response.json()
        else:
            return getErrorResponse()
    except:
        return getErrorResponse()


#TO fetch isochrone of a region for a specific time travel
@app.route("/isochroneAsync", methods=["GET"])
def isochroneAsync():
    baseUrl = getBaseURL("isochroneAsync")
    params = ["waypoint", "maxDistance", "distanceUnit", "optimize", "travelMode", "maxTime", "timeUnit", "dateTime"]
    queryString = ""

    for param in params:
        if param in request.args:
            queryString += param + "=" + request.args[param] + "&"

    queryString += "key="+getBingKey()
    baseUrl = baseUrl + "?" + queryString
    try:
        response = requests.get(baseUrl)

        requestId = response.json()["resourceSets"][0]["resources"][0]["requestId"]
        callbackTime = response.json()["resourceSets"][0]["resources"][0]["callbackInSeconds"]

        print(response.json()["resourceSets"][0]["resources"][0]["callbackUrl"])

        if response.status_code == 200:
            return {'requestId': requestId, 'callbackTime': callbackTime}
        else:
            print("failure")
            return getErrorResponse()
    except:
        return getErrorResponse()


@app.route("/isochroneCallback", methods=["GET"])
def checkCallback():
    requestId = request.args['requestId']
    callBackUrl = getBaseURL("IsochronesAsyncCallback") + "?requestId={}&key={}".format(requestId, getBingKey())
    response = requests.get(callBackUrl)
    try:
        callbackTime = response.json()["resourceSets"][0]["resources"][0]["callbackInSeconds"]
        if callbackTime < 0:
            resultUrl = response.json()["resourceSets"][0]["resources"][0]["resultUrl"]
            resp = requests.get(resultUrl)
            print(resp.json())
            return resp.json()
        else:
            return {'requestId': requestId, 'callbackTime': callbackTime}
    except:
        return getErrorResponse()

#To fetch all local business in a radius of X meters
#Params that can be passed to to the feautre 
#       type = to fetch types of data
#       userCircularMapView    = to pass lat, lang and radius range
@app.route("/business", methods=["GET"])
def business():
    baseUrl = getBaseURL("business")
    params = ["type", "userCircularMapView", "maxResults"]
    queryString = ""
    for param in params:
        if param in request.args:
            queryString += param+"="+request.args[param]+"&"

    queryString += "key="+getBingKey()
    baseUrl = baseUrl + "?" + queryString
    try:
        response = requests.get(baseUrl)
        if response.status_code == 200:
            return response.json()
        else:
            return getErrorResponse()
    except:
        return getErrorResponse()

@app.route("/map")
def map():
    return render_template("maps.html")

if __name__ =='__main__':  
    app.run(host='127.0.0.1', port=8080, debug=True)  

