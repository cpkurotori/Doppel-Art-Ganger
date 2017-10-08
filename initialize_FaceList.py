import httplib, urllib, base64, json

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '65fb1f6458eb4338a49b7c75e420eca2'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westus.api.cognitive.microsoft.com/face/v1.0'

# Request headers.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = urllib.urlencode({
    'faceListId': 'artwork',
})

body = "{'name':'artwork'}"

try:
    # Execute the REST API call and get the response.
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/facelists/%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
