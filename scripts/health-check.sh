#!/bin/bash
set -e

# ============================================================================
# Server Health Check
# ============================================================================
# Checks Docker, disk, memory, load, container health, and ports.
# Run on the server directly or via SSH:
#   ssh -i <your-key> <user>@<server_ip> "bash ~/projects/fastapi_app/scripts/health-check.sh"
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

echo "========================================="
echo "SERVER HEALTH CHECK"
echo "========================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="

# Check Docker
echo -e "\n[Docker Service]"
if systemctl is-active --quiet docker; then
    log_success "Docker is running"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    log_error "Docker is not running"
fi

# Check disk space
echo -e "\n[Disk Space]"
df -h / | tail -1 | awk '{print "Used: " $3 " / " $2 " (" $5 ")"}'
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    log_warning "Disk usage above 80%"
fi

# Check memory
echo -e "\n[Memory]"
free -h | grep Mem | awk '{print "Used: " $3 " / " $2}'

# Check system load
echo -e "\n[System Load]"
uptime | awk -F'load average:' '{print "Load Average:" $2}'

# Check Docker container health
echo -e "\n[Container Health]"
docker ps --filter "health=unhealthy" --format "{{.Names}}: {{.Status}}" | while read line; do
    if [ -n "$line" ]; then
        log_error "$line"
    fi
done || true

UNHEALTHY=$(docker ps --filter "health=unhealthy" -q | wc -l)
if [ "$UNHEALTHY" -eq 0 ]; then
    log_success "All containers are healthy"
fi

# Check critical ports
echo -e "\n[Network Ports]"
for port in 80 443 22; do
    if ss -tuln | grep -q ":$port "; then
        log_success "Port $port is open"
    else
        log_error "Port $port is not listening"
    fi
done

# Check firewall
echo -e "\n[Firewall]"
if systemctl is-active --quiet ufw; then
    log_success "UFW is active"
    ufw status | grep "Status:"
else
    log_warning "UFW is not active"
fi

echo -e "\n========================================="
echo "Health check complete"
echo "========================================="
