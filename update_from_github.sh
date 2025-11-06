#!/bin/bash

# Update learnGerman app from GitHub
# This script stops the service, pulls latest code, and restarts

echo "🛑 Stopping learnGerman service..."
launchctl unload ~/Library/LaunchAgents/com.learngerman.app.plist

echo "📥 Pulling latest code from GitHub..."
cd ~/learnGerman
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully updated from GitHub"
else
    echo "❌ Error pulling from GitHub"
    exit 1
fi

echo "🚀 Starting learnGerman service..."
launchctl load ~/Library/LaunchAgents/com.learngerman.app.plist

# Wait a moment for service to start
sleep 2

echo "🔍 Checking if service is running..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "✅ learnGerman is running on port 8000"
    echo "🌐 Access at: http://$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost"):8000"
else
    echo "❌ Service may not be running. Check logs:"
    echo "   tail ~/learnGerman/logs/error.log"
fi
