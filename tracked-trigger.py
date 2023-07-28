import sys
import requests
import json
import os

# Set variables
keyId = os.environ.get('SL_KEY_ID')
keySecret = os.environ.get('SL_KEY_SECRET')
baseURL = os.environ.get('SL_BASE_URL')
stack = sys.argv[1]
runId = sys.argv[2]
tokenMutatationVariables = {'keyId': keyId, 'keySecret': keySecret}
triggerVariables = {'stack': stack} 
runLogsVariables = {'stackId': stack, 'runId' : runId, 'state': "FINISHED", 'stateVersion' : "2", 'token' : ""}


#The mutation to get the Bearer Token
tokenMutation = """mutation GetSpaceliftToken($keyId: ID!, $keySecret: String!) {apiKeyUser(id: $keyId, secret: $keySecret) {jwt}}"""

#The mutation to trigger a tracked run based on ID
triggerMutation = """
mutation ($stack : ID!){
        runTrigger(stack: $stack) {
        id
        title
        type
    }
}
"""

logsQuery = """
query GetLogs($stackId: ID!, $runId: ID!, $state: RunState!, $stateVersion: Int, $token: String ) {
	stack(id: $stackId) {
		id
		run(id: $runId) {
			id
			logs(state: $state, stateVersion: $stateVersion token: $token) {
				exists
				finished
				expired
				hasMore
				messages {
					message
					__typename
				}
				nextToken
				__typename
			}
            state
			__typename
		}
		__typename
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
def triggerRun(trigger): 
    request = requests.post(baseURL, json={'query': trigger, 'variables': triggerVariables }, headers=headers)
    print(json.dumps(request.json(), indent=4))

def getRunLogs(logsQuery):    
    request = requests.post(baseURL, json={'query': logsQuery, 'variables': runLogsVariables }, headers=headers)
    print(json.dumps(request.json(), indent=4))

# Execute the API call
jwt = getSpaceliftToken()
headers = {"Authorization": f"Bearer {jwt}"}
# triggerRun(triggerMutation)

getRunLogs(logsQuery)