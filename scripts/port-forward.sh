#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_usage() {
    echo -e "${BLUE}Usage: $0 [service]${NC}"
    echo "Available services:"
    echo "  all       - Expose Web UI and all Observability tools (Background)"
    echo "  web       - Expose Web Frontend (localhost:8080)"
    echo "  gateway   - Expose Istio Ingress Gateway (localhost:8081)"
    echo "  kiali     - Expose Kiali Dashboard (localhost:20001)"
    echo "  grafana   - Expose Grafana (localhost:3000)"
    echo "  jaeger    - Expose Jaeger UI (localhost:16686)"
    echo "  prometheus- Expose Prometheus (localhost:9090)"
    echo "  stop      - Stop all background port-forwards"
}

port_forward() {
    local name=$1
    local ns=$2
    local res=$3
    local ports=$4
    local pid_file="/tmp/pf_${name}.pid"

    if [ -f "$pid_file" ]; then
        if kill -0 $(cat "$pid_file") 2>/dev/null; then
            echo -e "${YELLOW}⚠️  $name is already running (PID: $(cat $pid_file))${NC}"
            return
        else
             rm "$pid_file"
        fi
    fi

    echo -e "${GREEN}🔌 Forwarding $name -> $ports...${NC}"
    kubectl port-forward -n "$ns" "$res" "$ports" > /dev/null 2>&1 &
    echo $! > "$pid_file"
}

stop_all() {
    echo -e "${YELLOW}🛑 Stopping all port-forwards...${NC}"
    for pid_file in /tmp/pf_*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            echo "Killing PID $pid ($(basename $pid_file .pid | cut -d_ -f2))"
            kill $pid 2>/dev/null || true
            rm "$pid_file"
        fi
    done
    echo -e "${GREEN}✅ All stopped.${NC}"
}

SERVICE=$1

case "$SERVICE" in
    "web")
        port_forward "web" "santhe" "svc/web" "3000:3000"
        echo -e "${BLUE}🌍 Web UI: http://localhost:3000${NC}"
        ;;
    "gateway")
        port_forward "gateway" "istio-system" "svc/istio-ingressgateway" "8080:80"
        echo -e "${BLUE}🚪 API Gateway: http://localhost:8080${NC}"
        ;;
    "kiali")
        port_forward "kiali" "istio-system" "svc/kiali" "20001:20001"
        echo -e "${BLUE}🕸️  Kiali: http://localhost:20001${NC}"
        ;;
    "grafana")
        port_forward "grafana" "istio-system" "svc/grafana" "3000:3000"
        echo -e "${BLUE}📊 Grafana: http://localhost:3000${NC}"
        ;;
    "jaeger")
        port_forward "jaeger" "istio-system" "svc/tracing" "16686:80"
        echo -e "${BLUE}🕵️  Jaeger: http://localhost:16686${NC}"
        ;;
    "prometheus")
        port_forward "prometheus" "istio-system" "svc/prometheus" "9090:9090"
        echo -e "${BLUE}🔥 Prometheus: http://localhost:9090${NC}"
        ;;
    "postgres")
        port_forward "postgres" "database" "svc/postgres-postgresql" "5432:5432"
        echo -e "${BLUE}🐘 Postgres: localhost:5432${NC}"
        ;;
    "all")
        $0 web
        $0 gateway
        $0 kiali
        $0 grafana
        $0 jaeger
        $0 prometheus
        echo -e "${GREEN}✅ All services exposed!${NC}"
        ;;
    "stop")
        stop_all
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
