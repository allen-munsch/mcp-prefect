#!/bin/bash
set -e

echo "🚀 Setting up Prefect MCP with ToolHive"

# Configuration
PREFECT_API_URL="${PREFECT_API_URL:-http://localhost:4200/api}"
OPENAPI_FILE="prefect-openapi.json"
IMAGE_NAME="prefect-mcp"
SERVER_NAME="prefect-mcp-$(date +%s)"  # Unique name to avoid conflicts

# Function to cleanup any existing instances
cleanup_instances() {
    echo "🧹 Cleaning up existing instances..."
    
    # Stop all prefect-mcp related containers
    docker ps -a --filter "name=prefect-mcp" --format "{{.Names}}" | while read container; do
        echo "🛑 Stopping container: $container"
        docker stop "$container" 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
    done
    
    # Stop ToolHive workloads
    thv list 2>/dev/null | grep "prefect-mcp" | awk '{print $1}' | while read workload; do
        echo "🛑 Stopping workload: $workload"
        thv stop "$workload" 2>/dev/null || true
    done
    
    # Clear any cached configurations
    if [ -d "$HOME/.local/share/toolhive" ]; then
        echo "🧹 Cleaning ToolHive cache..."
        find "$HOME/.local/share/toolhive" -name "*prefect-mcp*" -delete 2>/dev/null || true
    fi
    
    sleep 2
}

# Function to check if server is running
is_server_running() {
    if docker ps --format "{{.Names}}" | grep -q "prefect-mcp"; then
        return 0
    else
        return 1
    fi
}

# Function to start server with fresh approach
start_server_fresh() {
    echo "🚀 Starting fresh MCP server..."
    
    cleanup_instances
    
    # Use a unique name to avoid conflicts
    local unique_name="prefect-mcp-$(date +%s)"
    echo "🔧 Using unique name: $unique_name"
    
    # Run directly with docker first to test
    echo "🧪 Testing container directly..."
    docker run -d --rm \
        --name "$unique_name" \
        -v "$(pwd)/$OPENAPI_FILE:/server/$OPENAPI_FILE:ro" \
        -e "AUTO_MCP_SWAGGER_FILE=/server/$OPENAPI_FILE" \
        "$IMAGE_NAME:latest"
    
    sleep 5
    
    if docker ps | grep -q "$unique_name"; then
        echo "✅ Container started successfully"
        echo "📋 Container logs:"
        docker logs "$unique_name" 2>&1 | tail -10
        
        # Stop the test container
        docker stop "$unique_name"
        
        # Now run with ToolHive
        echo "🚀 Starting with ToolHive..."
        thv run "$IMAGE_NAME:latest" \
            --name "prefect-mcp" \
            --volume "$(pwd)/$OPENAPI_FILE:/server/$OPENAPI_FILE:ro" \
            --env "AUTO_MCP_SWAGGER_FILE=/server/$OPENAPI_FILE" \
            --foreground &
        
        local SERVER_PID=$!
        sleep 10
        
        if is_server_running; then
            echo "✅ Server started successfully with PID: $SERVER_PID"
            return 0
        else
            echo "❌ Server failed to start"
            kill $SERVER_PID 2>/dev/null
            return 1
        fi
    else
        echo "❌ Container test failed"
        return 1
    fi
}

# Function to start server (simple approach)
start_server_simple() {
    echo "🚀 Starting server (simple approach)..."
    
    # Clean up first
    cleanup_instances
    
    # Run with a slight delay
    sleep 2
    
    # Start with ToolHive in foreground
    thv run "$IMAGE_NAME:latest" \
        --name "prefect-mcp" \
        --volume "$(pwd)/$OPENAPI_FILE:/server/$OPENAPI_FILE:ro" \
        --env "AUTO_MCP_SWAGGER_FILE=/server/$OPENAPI_FILE" \
        --foreground &
    
    local SERVER_PID=$!
    echo "📝 Server starting with PID: $SERVER_PID"
    
    # Wait and check
    sleep 10
    if is_server_running; then
        echo "✅ Server started successfully"
        echo "💡 Server is running in background with PID: $SERVER_PID"
        echo "💡 Use '$0 logs' to see logs"
        echo "💡 Use '$0 stop' to stop the server"
        return 0
    else
        echo "❌ Server failed to start"
        kill $SERVER_PID 2>/dev/null
        return 1
    fi
}

# Function to start server (direct docker)
start_server_docker() {
    echo "🚀 Starting server with Docker directly..."
    
    cleanup_instances
    
    docker run -d \
        --name "prefect-mcp" \
        -v "$(pwd)/$OPENAPI_FILE:/server/$OPENAPI_FILE:ro" \
        -e "AUTO_MCP_SWAGGER_FILE=/server/$OPENAPI_FILE" \
        "$IMAGE_NAME:latest"
    
    sleep 5
    
    if is_server_running; then
        echo "✅ Server started successfully with Docker"
        echo "📋 Container status:"
        docker ps --filter "name=prefect-mcp" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        return 0
    else
        echo "❌ Docker start failed"
        docker logs "prefect-mcp" 2>&1 | tail -10
        return 1
    fi
}

# Function to stop server
stop_server() {
    echo "🛑 Stopping server..."
    
    # Stop ToolHive workload
    thv stop "prefect-mcp" 2>/dev/null || true
    
    # Stop Docker container
    docker stop "prefect-mcp" 2>/dev/null || true
    docker rm "prefect-mcp" 2>/dev/null || true
    
    # Additional cleanup
    cleanup_instances
    
    echo "✅ Server stopped"
}

# Function to show status
show_status() {
    echo "📊 Server Status:"
    
    # Check ToolHive
    echo "🔍 ToolHive workloads:"
    thv list 2>/dev/null | grep -E "(NAME|prefect-mcp)" || echo "  No prefect-mcp workloads found"
    
    echo ""
    echo "🔍 Docker containers:"
    docker ps --filter "name=prefect-mcp" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || echo "  No prefect-mcp containers found"
    
    echo ""
    if is_server_running; then
        echo "✅ Server is RUNNING"
        echo "💡 Use '$0 logs' to see logs"
    else
        echo "❌ Server is NOT RUNNING"
        echo "💡 Use '$0 start-simple' to start the server"
    fi
}

# Function to show logs
show_logs() {
    if is_server_running; then
        echo "📋 Server logs:"
        docker logs "prefect-mcp" --tail 20 2>/dev/null || \
        thv logs "prefect-mcp" --tail 20 2>/dev/null || \
        echo "No logs available"
    else
        echo "❌ Server is not running"
    fi
}

# Main execution
case "${1:-}" in
    start|start-simple)
        start_server_simple
        ;;
    start-fresh)
        start_server_fresh
        ;;
    start-docker)
        start_server_docker
        ;;
    stop)
        stop_server
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    cleanup)
        cleanup_instances
        ;;
    test)
        echo "🧪 Testing auto-mcp container..."
        docker run --rm \
            -v "$(pwd)/$OPENAPI_FILE:/server/$OPENAPI_FILE:ro" \
            -e "AUTO_MCP_SWAGGER_FILE=/server/$OPENAPI_FILE" \
            "$IMAGE_NAME:latest" \
            --mode=stdio
        ;;
    *)
        echo "Usage: $0 {start|start-fresh|start-docker|stop|status|logs|cleanup|test}"
        echo ""
        echo "  start        - Start server with ToolHive (simple)"
        echo "  start-fresh  - Clean and start fresh"
        echo "  start-docker - Start with Docker directly (no ToolHive)"
        echo "  stop         - Stop server"
        echo "  status       - Show server status"
        echo "  logs         - Show server logs"
        echo "  cleanup      - Clean up all instances"
        echo "  test         - Test container directly"
        echo ""
        show_status
        ;;
esac