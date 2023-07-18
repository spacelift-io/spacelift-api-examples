import sys
import requests
import json
import os

# Set variables
keyId = os.environ.get('SL_KEY_ID')
keySecret = os.environ.get('SL_KEY_SECRET')
baseURL = os.environ.get('SL_BASE_URL')
tokenMutatationVariables = {'keyId': keyId, 'keySecret': keySecret}

#The mutation to get the Bearer Token
tokenMutation = """mutation GetSpaceliftToken($keyId: ID!, $keySecret: String!) {apiKeyUser(id: $keyId, secret: $keySecret) {jwt}}"""

#The mutation to trigger a track run based on ID
triggerMutation = """
mutation {
        runTrigger(stack: "tf-aws") {
        id
        title
        type
    }
}
"""

# function to create the jwt(spacelift token) for the header
def getSpaceliftToken():
    request = requests.post(baseURL, json={'query': tokenMutation, 'variables': tokenMutatationVariables})
    response = request.json()
    token = response['data']['apiKeyUser']['jwt']
    return token

# function to make the API call
def runQuery(trigger): 
    request = requests.post(baseURL, json={'query': trigger}, headers=headers)
    print(json.dumps(request.json(), indent=4))

# Execute the API call
jwt = getSpaceliftToken()
headers = {"Authorization": f"Bearer {jwt}"}
runQuery(trigger)