# tracer/dns.py
import ipaddress

class DNSResolver:
    def __init__(self, records):
        """
        records: list of dicts like:
          { "type": "A", "name": "example.com", "value": "192.168.2.10" }
          { "type": "CNAME", "name": "www.example.com", "value": "example.com" }
        """
        self.records = records

    def resolve_with_trace(self, name, max_depth=10):
        trace = []
        current = name
        depth = 0
        while depth < max_depth:
            depth += 1
            rec = self._find_record(current)
            if not rec:
                trace.append({"location": "DNS Resolver", "action": f"{current} -> NXDOMAIN (no record)"})
                return None, trace

            if rec["type"] == "A":
                trace.append({"location": "DNS Resolver", "action": f"Resolved {name} to {rec['value']} (A record)"})
                return rec["value"], trace
            elif rec["type"] == "CNAME":
                trace.append({"location": "DNS Resolver", "action": f"{current} is CNAME -> {rec['value']}"})
                current = rec["value"]
                continue
            else:
                trace.append({"location": "DNS Resolver", "action": f"Unsupported record type {rec['type']} for {current}"})
                return None, trace
        trace.append({"location": "DNS Resolver", "action": "CNAME resolution depth exceeded"})
        return None, trace

    # tracer/dns.py

    def _find_record(self, name):
        # The 'name' argument is the hostname we are searching for (e.g., 'www.example.com')
        search_name = name.strip().lower() # Normalize the incoming search string
        
        for r in self.records:
            # Normalize the name from the configuration file before comparison
            record_name = r["name"].strip().lower() 
            
            if record_name == search_name:
                return r.copy()
        return None
