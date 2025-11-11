#!/bin/bash
# scripts/generate-openapi.sh

echo "🔧 Generating Prefect OpenAPI specification..."

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "Checking Prefect server health (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)..."
    
    if curl -s http://prefect-server:4200/api/health >/dev/null; then
        echo "✅ Prefect server is healthy, generating OpenAPI spec..."
        curl -s http://prefect-server:4200/api/openapi.json > /output/prefect-openapi.json
        
        if [ -s /output/prefect-openapi.json ]; then
            echo "✅ OpenAPI spec generated successfully"
            echo "📄 File size: $(wc -c < /output/prefect-openapi.json) bytes"
            
            # Fix compatibility issues
            if command -v jq >/dev/null 2>&1; then
                echo "🛠️ Fixing OpenAPI spec compatibility..."
                jq 'walk(if type == "object" then del(.exclusiveMinimum?) | del(.exclusiveMaximum?) else . end)' \
                   /output/prefect-openapi.json > /output/prefect-openapi-fixed.json && \
                mv /output/prefect-openapi-fixed.json /output/prefect-openapi.json
                echo "✅ OpenAPI spec fixed for auto-mcp compatibility"
            fi
            
            exit 0
        else
            echo "❌ OpenAPI spec is empty"
            exit 1
        fi
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 2
done

echo "❌ Prefect server not ready after $MAX_RETRIES attempts"
exit 1