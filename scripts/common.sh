#!/bin/bash
# Common utility functions for scripts

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
check_status() {
    if [ $? -eq 0 ]; then
        print_status "$1"
    else
        print_error "$1 Failed"
        exit 1
    fi
}

# Detect changed services using git
get_changed_services() {
    local changed_services=""
    # Staged and unstaged changes
    changed_services=$(git diff --name-only HEAD 2>/dev/null | grep "^services/" | cut -d'/' -f2 | sort -u)
    changed_services="$changed_services $(git diff --cached --name-only 2>/dev/null | grep "^services/" | cut -d'/' -f2 | sort -u)"
    
    # Return unique sorted list
    echo "$changed_services" | tr ' ' '\n' | sort -u | tr '\n' ' '
}
