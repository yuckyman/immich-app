#!/bin/bash
# Monitor the application logs in real-time

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/app_$(date +%Y%m%d).log"

if [ ! -f "$LOG_FILE" ]; then
    echo "Waiting for log file to be created..."
    # Wait for log file to exist
    while [ ! -f "$LOG_FILE" ]; do
        sleep 1
    done
fi

echo "Monitoring: $LOG_FILE"
echo "Press Ctrl+C to stop"
echo "---"
tail -f "$LOG_FILE"

