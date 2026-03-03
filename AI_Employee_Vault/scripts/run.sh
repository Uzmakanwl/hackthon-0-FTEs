#!/bin/bash
# AI Employee - Bronze Tier Startup Script for Unix/Mac
# This script starts both the File Watcher and Orchestrator

echo "============================================"
echo "AI Employee - Bronze Tier"
echo "============================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_DIR="$(dirname "$SCRIPT_DIR")"

# Create DropFolder if it doesn't exist
if [ ! -d "$VAULT_DIR/DropFolder" ]; then
    mkdir -p "$VAULT_DIR/DropFolder"
    echo "Created DropFolder: $VAULT_DIR/DropFolder"
fi

echo "Vault Directory: $VAULT_DIR"
echo "Drop Folder: $VAULT_DIR/DropFolder"
echo ""

# Start File Watcher in background
echo "Starting File System Watcher..."
cd "$SCRIPT_DIR"
python filesystem_watcher.py "$VAULT_DIR" "$VAULT_DIR/DropFolder" &
WATCHER_PID=$!
echo "File Watcher Started (PID: $WATCHER_PID)"

# Wait a moment for watcher to start
sleep 2

# Start Orchestrator in foreground
echo "Starting Orchestrator..."
echo ""
python orchestrator.py "$VAULT_DIR"

# Cleanup on exit
echo ""
echo "Stopping File Watcher..."
kill $WATCHER_PID 2>/dev/null

echo "============================================"
echo "AI Employee Stopped"
echo "============================================"
