from flask import Flask, request, jsonify
import json
import ipaddress
import os


# from tracer.dns import DNSResolver
# from tracer.router import RouterEngine
# from tracer.firewall import FirewallEngine 

# Assume the following classes are correctly imported from the 'tracer' package
class DNSResolver:
    def __init__(self, config):
        pass # Mock
    def resolve_with_trace(self, hostname):
        return None, [] # Mock

class RouterEngine:
    def __init__(self, config):
        pass # Mock
    def find_router_for_host(self, ip):
        return None # Mock

class FirewallEngine:
    def __init__(self, config):
        pass # Mock
    def evaluate_packet(self, protocol, src_ip, dst_ip, dst_port, router_name):
        return "ALLOW", "Packet passed firewall" # Mock


app = Flask(__name__)


CONFIG_PATH = os.environ.get("PACKET_TRACER_CONFIG", "config/scenario-complex.json")
try:
    with open(CONFIG_PATH) as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    print(f"ERROR: Configuration file not found at {CONFIG_PATH}")
    exit(1)


# The original code had these imports uncommented. Using mock classes for display clarity.
# dns = DNSResolver(CONFIG.get("dns", [])) 
# firewall = FirewallEngine(CONFIG.get("firewall", []))
# router_engine = RouterEngine(CONFIG.get("routers", {}))

# For a functional simulation, ensure the actual imports are used:
from tracer.dns import DNSResolver
from tracer.router import RouterEngine
from tracer.firewall import FirewallEngine 

dns = DNSResolver(CONFIG.get("dns", []))
firewall = FirewallEngine(CONFIG.get("firewall", []))
router_engine = RouterEngine(CONFIG.get("routers", {}))


@app.route("/trace", methods=["POST"])
def trace_packet():
    """ Runs the multi-hop packet trace simulation. """
    payload = request.get_json(force=True)
    
    required = ["src_ip", "dst", "dst_port", "protocol", "ttl"]
    for r in required:
        if r not in payload:
            return jsonify({"error": f"missing field {r}"}), 400

    src_ip = payload["src_ip"]
    dst = payload["dst"]
    dst_port = int(payload["dst_port"])
    protocol = payload["protocol"].upper()
    ttl = int(payload["ttl"])

    trace = []
    current_ttl = ttl

    # Step 1: Resolve DNS if needed
    try:
        ipaddress.ip_address(dst)
        dst_ip = dst
        trace.append({"location": "Client", "action": f"Destination provided as IP {dst_ip}"})
    except ValueError:
        trace.append({"location": "Client", "action": f"Resolving hostname {dst} via DNS"})
        
        resolved, dns_events = dns.resolve_with_trace(dst)
        trace.extend(dns_events)
        
        if not resolved:
            trace.append({"location": "DNS Resolver", "action": "NXDOMAIN — name does not exist"})
            return jsonify(trace), 200
        dst_ip = resolved
    
    # --- Start Simulation ---
    trace.append({"location": "Client", "action": f"Starting packet from {src_ip} to {dst_ip}:{dst_port} protocol={protocol} ttl={current_ttl}"})

    # Step 2: Find first hop router
    current_router = router_engine.find_router_for_host(src_ip)
    if not current_router:
        trace.append({"location": "Network", "action": "No directly connected router found for source; cannot send packet"})
        return jsonify(trace), 200

    # Step 3: Simulate Hops (The main loop)
    visited_routers = []
    
    while True:
        if current_ttl <= 0:
            trace.append({"location": "Simulation", "action": "Time to Live exceeded"})
            break

        current_ttl -= 1

        trace.append({"location": current_router.name, "action": f"Packet arrived at {current_router.name} (ttl={current_ttl})"})

        # A. Apply firewall rules
        fw_action, fw_event = firewall.evaluate_packet(
            protocol=protocol, src_ip=src_ip, dst_ip=dst_ip, dst_port=dst_port, router_name=current_router.name
        )
        trace.append({"location": current_router.name, "action": fw_event})
        if fw_action == "DENY":
            trace.append({"location": current_router.name, "action": f"Packet blocked by firewall on {current_router.name}"})
            break

        # B. Router makes routing decision (LPM)
        route_entry = current_router.longest_prefix_match(dst_ip)
        if not route_entry:
            trace.append({"location": current_router.name, "action": "No route to host (Destination Unreachable)"})
            break

        next_hop = route_entry["next_hop"]
        out_if = route_entry.get("interface", "unknown")
        trace.append({"location": current_router.name, "action": f"Forwarded to next-hop {next_hop} via {out_if} (route {route_entry['dest']})"})

        # C. Check for final destination delivery
        try:
            if ipaddress.ip_address(next_hop) == ipaddress.ip_address(dst_ip):
                trace.append({"location": "Destination", "action": f"Packet delivered to {dst_ip}:{dst_port}"})
                break
        except ValueError:
            pass
        
        # D. Find the next router for the hop
        next_router = router_engine.find_router_by_interface(next_hop)
        if not next_router:
            
            trace.append({"location": "Gateway", "action": "Packet forwarded to an external gateway; trace terminated (Assumed delivery/unreachability outside simulation)"})
            break

        # E. Loop prevention
        if next_router.name in visited_routers:
            trace.append({"location": "Simulation", "action": "Routing loop detected; terminating"})
            break
        visited_routers.append(next_router.name)
        current_router = next_router

    return jsonify(trace), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)