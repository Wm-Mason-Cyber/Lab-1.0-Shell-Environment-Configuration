#!/bin/bash
if [ -z "$TARGET_GATEWAY" ]; then
    echo "Error: TARGET_GATEWAY environment variable is not set."
    echo "Fix:  export TARGET_GATEWAY=\"http://<Instructor_IP>:8080\""
    exit 1
fi

USERNAME=$(whoami)
TIMESTAMP=$(date -Iseconds)
read -p "Enter your first name: " FIRST_NAME
read -p "Enter your last name: " LAST_NAME
read -p "Enter your class period number: " CLASS_PERIOD

echo "Sending to $TARGET_GATEWAY ..."
RESPONSE=$(curl -s -X POST "$TARGET_GATEWAY/lab-1-0-2" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"first_name\": \"$FIRST_NAME\", \"last_name\": \"$LAST_NAME\", \"timestamp\": \"$TIMESTAMP\", \"period\": \"$CLASS_PERIOD\"}")

echo "$RESPONSE"
