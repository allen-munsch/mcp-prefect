#!/bin/bash
# fix-openapi.sh

echo "🔧 Fixing OpenAPI spec compatibility for auto-mcp..."

INPUT_FILE="prefect-openapi.json"
FIXED_FILE="prefect-openapi-fixed.json"

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Input file not found: $INPUT_FILE"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "❌ jq is required but not installed."
    exit 1
fi

echo "📄 Original file: $(wc -c < "$INPUT_FILE") bytes"

# Fix the OpenAPI spec compatibility issues
echo "🛠️ Fixing exclusiveMinimum/exclusiveMaximum fields..."
jq '
walk(
    if type == "object" then 
        with_entries(
            if .key == "exclusiveMinimum" and (.value | type == "number") then
                {key: "minimum", value: .value}
            elif .key == "exclusiveMaximum" and (.value | type == "number") then
                {key: "maximum", value: .value}
            else
                .
            end
        )
    else
        .
    end
) |
walk(
    if type == "object" and has("exclusiveMinimum") and (.exclusiveMinimum | type == "number") then
        . + {minimum: .exclusiveMinimum} | del(.exclusiveMinimum)
    elif type == "object" and has("exclusiveMaximum") and (.exclusiveMaximum | type == "number") then
        . + {maximum: .exclusiveMaximum} | del(.exclusiveMaximum)
    else
        .
    end
)
' "$INPUT_FILE" > "$FIXED_FILE"

if [ $? -eq 0 ] && [ -s "$FIXED_FILE" ]; then
    echo "✅ Fixed OpenAPI spec created: $FIXED_FILE"
    echo "📄 New file size: $(wc -c < "$FIXED_FILE") bytes"
    
    # Replace the original file
    mv "$FIXED_FILE" "$INPUT_FILE"
    echo "✅ OpenAPI spec fixed and replaced"
else
    echo "❌ Failed to fix OpenAPI spec"
    exit 1
fi