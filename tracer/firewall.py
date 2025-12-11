# tracer/firewall.py
import ipaddress

def parse_port_spec(spec):
    """
    spec can be integer, "80", or "1000-2000"
    return a tuple (min,max)
    """
    if isinstance(spec, int):
        return (int(spec), int(spec))
    if isinstance(spec, str) and "-" in spec:
        a,b = spec.split("-",1)
        return (int(a.strip()), int(b.strip()))
    return (int(spec), int(spec))

class FirewallEngine:
    def __init__(self, rules):
        """
        rules: ordered list of dict:
         { "action": "allow"/"deny", "protocol": "TCP"/"UDP"/"ANY", "src": "192.168.1.0/24" or "any", "dst_port": 80 or "1000-2000", "apply_to": "Router-1" (optional) }
        """
        self.rules = []
        for r in rules:
            rule = r.copy()
            rule["protocol"] = rule.get("protocol", "ANY").upper()
            src = rule.get("src", "any")
            if src != "any":
                rule["src_net"] = ipaddress.ip_network(src)
            else:
                rule["src_net"] = None
            rule["dst_port_range"] = parse_port_spec(rule.get("dst_port", "any")) if rule.get("dst_port", "any") != "any" else (0, 65535)
            self.rules.append(rule)

    def evaluate_packet(self, protocol, src_ip, dst_ip, dst_port, router_name=None):
        """
        Return ("ALLOW"/"DENY"/"NO_MATCH", "description")
        Only rules that have apply_to==None or apply_to==router_name are considered.
        """
        proto = protocol.upper()
        sip = ipaddress.ip_address(src_ip)
        for idx, r in enumerate(self.rules, start=1):
            apply_to = r.get("apply_to")
            if apply_to and router_name and apply_to != router_name:
                continue
            # protocol match
            if r["protocol"] != "ANY" and r["protocol"] != proto:
                continue
            # src match
            if r["src_net"] is not None:
                if sip not in r["src_net"]:
                    continue
            # port match
            low, high = r["dst_port_range"]
            if not (low <= int(dst_port) <= high):
                continue
            action = r["action"].upper()
            return ("DENY" if action == "DENY" else "ALLOW", f"Matched rule #{idx} ({action}) on router {apply_to or 'global'}")
        return ("NO_MATCH", "No firewall rule matched (default allow)")
