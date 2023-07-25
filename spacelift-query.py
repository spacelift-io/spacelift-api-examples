import sys
import requests
import json
import os

# Set variables
keyId = os.environ.get('SPACELIFT_KEY_ID')
keySecret = os.environ.get('SPACELIFT_KEY_SECRET')
baseURL = os.environ.get('SPACELIFT_BASE_URL')
mutatationVariables = {'keyId': keyId, 'keySecret': keySecret}

#The GraphQL mutation to get the Bearer Token
mutation = """mutation GetSpaceliftToken($keyId: ID!, $keySecret: String!) {apiKeyUser(id: $keyId, secret: $keySecret) {jwt}}"""

# ---The API call---
# By default this will be a basic Stack query
# unless you pass in a custom request as an argument
query = sys.argv[1] if len(sys.argv) > 1 else """{stacks {id name space administrative state}}"""

# function to create the jwt(spacelift token) for the header
def getSpaceliftToken():
    request = requests.post(baseURL, json={'query': mutation, 'variables': mutatationVariables})
    response = request.json()
    token = response['data']['apiKeyUser']['jwt']
    return token

# function to make the API call
def runQuery(query): 
    request = requests.post(baseURL, json={'query': query}, headers=headers)
    print(json.dumps(request.json(), indent=4))

# Execute the API call
jwt = getSpaceliftToken()
headers = {"Authorization": f"Bearer {jwt}"}
runQuery(query)
