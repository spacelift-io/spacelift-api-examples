#!/bin/sh

# Usage:
# ./api.sh <API_ENDPOINT> <API_KEY_ID> <API_KEY_SECRET> <API_PAYLOAD_PATH>

API_ENDPOINT=$1
API_KEY_ID=$2
API_KEY_SECRET=$3
API_PAYLOAD_PATH=$4

API_TOKEN_PAYLOAD=$(cat <<-EOM
{
  "query": "mutation GetSpaceliftToken(\$apiKeyId: ID!, \$apiKeySecret: String!) {apiKeyUser(id: \$apiKeyId, secret: \$apiKeySecret) {jwt}}",
  "variables": {"apiKeyId": "$API_KEY_ID", "apiKeySecret": "$API_KEY_SECRET"}
}
EOM
)

API_TOKEN=$(curl $API_ENDPOINT \
  --data "$API_TOKEN_PAYLOAD"  \
  --header 'content-type: application/json' \
  --request POST \
  --show-error \
  --silent \
  | jq -r '.data.apiKeyUser.jwt'
)

curl $API_ENDPOINT \
  --data "@$API_PAYLOAD_PATH"  \
  --header "Authorization: Bearer $API_TOKEN" \
  --header 'Content-Type: application/json' \
  --request POST \
  --show-error \
  --silent
