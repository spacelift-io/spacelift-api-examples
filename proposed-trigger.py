import sys
import requests
import json
import os

# Set variables
keyId = os.environ.get('SL_KEY_ID')
keySecret = os.environ.get('SL_KEY_SECRET')
baseURL = os.environ.get('SL_BASE_URL')
stack = sys.argv[1]
commitSha = sys.argv[2]
runId = sys.argv[3]
tokenMutatationVariables = {'keyId': keyId, 'keySecret': keySecret}
triggerVariables = {'stack': stack, 'commitSha': commitSha, 'runType': "PROPOSED"} 
runLogsVariables = {'stackId': stack, 'runId' : runId, 'state': "FINISHED", }
#The mutation to get the Bearer Token
tokenMutation = """mutation GetSpaceliftToken($keyId: ID!, $keySecret: String!) {apiKeyUser(id: $keyId, secret: $keySecret) {jwt}}"""

#The mutation to trigger a tracked run based on ID
triggerMutation = """
mutation ($stack : ID!, $commitSha : String, $runType : RunType){
        runTrigger(stack: $stack, commitSha: $commitSha, runType: $runType) {
        id
        title
        type
    }
}
"""

logsQuery = """
query GetLogs($stackId: ID!, $runId: ID!, $state: RunState!, $token: String, $stateVersion: Int ) {
	stack(id: $stackId) {
		id
		run(id: $runId) {
			id
			logs(state: $state, token: $token, stateVersion: $stateVersion) {
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
def triggerRun(triggerMutation): 
    request = requests.post(baseURL, json={'query': triggerMutation, 'variables': triggerVariables }, headers=headers)
    print(json.dumps(request.json(), indent=4))

def getRunLogs(logsQuery):    
    request = requests.post(baseURL, json={'query': logsQuery, 'variables': runLogsVariables }, headers=headers)
    print(json.dumps(request.json(), indent=4))

# Execute the API call
jwt = getSpaceliftToken()
headers = {"Authorization": f"Bearer {jwt}"}
triggerRun(triggerMutation)
getRunLogs(logsQuery)