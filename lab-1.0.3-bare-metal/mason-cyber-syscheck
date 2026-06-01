#!/bin/bash
echo "=== MASON CYBER SYSTEM CHECK ==="
echo "User:     $(whoami)@$(hostname)"
echo "Date:     $(date)"
echo ""
echo "--- Network Interfaces ---"
ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print "  " $NF ": " $2}'
echo "Default Gateway: $(ip route | grep default | awk '{print $3}')"
echo ""
echo "--- Disk Usage ---"
df -h / | tail -1 | awk '{print "  Root: " $3 " used of " $2 " (" $5 " full)"}'
echo ""
echo "--- Local User Accounts ---"
awk -F: '$3 >= 1000 && $3 < 65534 {print "  " $1 " (uid=" $3 ")"}' /etc/passwd
echo ""
echo "--- Currently Logged In ---"
who | awk '{print "  " $1 " on " $2}'
echo "================================="
