# Usage:
#  - Run `pip install -r requirements.txt` to install dependencies
#  - Run `python trigger-run.py <STACK ID> [<COMMIT SHA>]`
# If a commit SHA is provided, a proposed run will be triggered. Otherwise, it will be a tracked run.

from urllib.parse import urlparse
import os
import sys
import requests

api_key_endpoint = os.environ.get("SPACELIFT_API_KEY_ENDPOINT")
api_key_id = os.environ.get("SPACELIFT_API_KEY_ID")
api_key_secret = os.environ.get("SPACELIFT_API_KEY_SECRET")
url_parts = urlparse(api_key_endpoint)
base_url = f"{url_parts.scheme}://{url_parts.hostname}"

# The mutation to get the Bearer Token
token_mutation = """
mutation GetSpaceliftToken($apiKeyId: ID!, $apiKeySecret: String!) {
  apiKeyUser(id: $apiKeyId, secret: $apiKeySecret) {
    jwt
  }
}
"""
token_mutation_variables = {"apiKeyId": api_key_id, "apiKeySecret": api_key_secret}

# The mutation to trigger a proposed run based on the stack ID and the commit hash
trigger_mutation = """
mutation ($stackId: ID!, $commitSha: String, $runType: RunType){
  runTrigger(stack: $stackId, commitSha: $commitSha, runType: $runType) {
    id
    title
    type
  }
}
"""

if len(sys.argv) > 1:
    stack_id = sys.argv[1]
else:
    print("Stack ID is missing")
    exit(1)

# Trigger a proposed run is a commit SHA is provided...
if len(sys.argv) > 2:
    commit_sha = sys.argv[2]
    trigger_mutation_variables = {
        "commitSha": commit_sha,
        "runType": "PROPOSED",
        "stackId": stack_id,
    }
    print(f"Trigerring a proposed run for stack {stack_id} and commit {commit_sha}")
# ... trigger a tracked run otherwise
else:
    trigger_mutation_variables = {
        "runType": "TRACKED",
        "stackId": stack_id,
    }
    print(f"Trigerring a tracked run for stack {stack_id}")


def get_jwt_token():
    request = requests.post(
        api_key_endpoint,
        json={"query": token_mutation, "variables": token_mutation_variables},
    )
    response = request.json()
    return response["data"]["apiKeyUser"]["jwt"]


def execute_query(jwt_token, query, variables):
    headers = {"Authorization": f"Bearer {jwt_token}"}

    request = requests.post(api_key_endpoint, json={"query": query, "variables": variables}, headers=headers)

    return request.json()


# Execute the API call
jwt_token = get_jwt_token()
result = execute_query(
    jwt_token=jwt_token,
    query=trigger_mutation,
    variables=trigger_mutation_variables,
)
print(f"URL for the run: {base_url}/stack/{stack_id}/run/{result['data']['runTrigger']['id']}")
