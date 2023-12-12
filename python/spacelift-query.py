# Usage:
#  - Run `pip install -r requirements.txt` to install dependencies
#  - Run `python spacelift-query.py`

import json
import os
import requests
import sys
from pprint import pprint

api_key_endpoint = os.environ.get("SPACELIFT_API_KEY_ENDPOINT")
api_key_id = os.environ.get("SPACELIFT_API_KEY_ID")
api_key_secret = os.environ.get("SPACELIFT_API_KEY_SECRET")

# The mutation to get the Bearer Token
token_mutation = """
mutation GetSpaceliftToken($apiKeyId: ID!, $apiKeySecret: String!) {
apiKeyUser(id: $apiKeyId, secret: $apiKeySecret) {
    jwt
}
}
"""
token_mutation_variables = {"apiKeyId": api_key_id, "apiKeySecret": api_key_secret}

# By default this will be a basic Stack query unless you pass in a custom request as an argument
if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    query = """
{
stacks {
    id
    name
    space
    administrative
    state
}
}
"""

# Use query variables if provided
if len(sys.argv) > 2:
    query_variables = json.loads(sys.argv[2])
else:
    query_variables = None


def get_jwt_token():
    response = requests.post(
        api_key_endpoint,
        json={"query": token_mutation, "variables": token_mutation_variables},
    )
    return response.json()["data"]["apiKeyUser"]["jwt"]


def execute_query(jwt_token, query, variables):
    headers = {"Authorization": f"Bearer {jwt_token}"}

    response = requests.post(api_key_endpoint, json={"query": query, "variables": variables}, headers=headers)

    return response.json()


# Execute the API call
jwt_token = get_jwt_token()
result = execute_query(
    jwt_token=jwt_token,
    query=query,
    variables=query_variables,
)
pprint(result)
