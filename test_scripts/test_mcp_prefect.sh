#!/bin/bash

SERVER="http://127.0.0.1:8000"

# Create initialize request
INIT_REQUEST=$(cat <<EOF
{
  "jsonrpc": "2.0",
  "id": "$(date +%s)",
  "method": "initialize",
  "params": {
    "clientInfo": {"name": "test-client", "version": "1.0.0"},
    "protocolVersion": "1.0.0",
    "capabilities": {"sampling": {}, "tools": {}}
  }
}
EOF
)

# URL encode the request
ENCODED_REQUEST=$(echo "$INIT_REQUEST" | jq -r @uri)

echo "Testing SSE connection with initialize..."
curl -NL -H "Accept: text/event-stream" "${SERVER}/sse?request=${ENCODED_REQUEST}"
