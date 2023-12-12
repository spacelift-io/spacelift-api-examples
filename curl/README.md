# cURL Example

# Usage

- Edit the [`get_stack.json`](./get_stack.json) example file to replace the `<STACK ID>` placeholder with a stack ID or create a new file from scratch with the GraphQL operation in the `query` property and variables, if any, in the `variables` property.
- Run `./api.sh <API_ENDPOINT> <API_KEY_ID> <API_KEY_SECRET> <API_PAYLOAD_PATH>` after replacing the placeholders:
    - `<API_ENDPOINT>`: Spacelift API endpoint (e.g. `https://example.app.spacelift.io/graphql`).
    - `<API_KEY_ID>`: Spacelift API key ID.
    - `<API_KEY_SECRET>`: Spacelift API key secret.
    - `<API_PAYLOAD_PATH>`: Path to the JSON file that contains the API call payload (e.g. `get_stack.json`).
