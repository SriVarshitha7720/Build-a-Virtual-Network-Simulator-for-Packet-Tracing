# tracer/router.py
import ipaddress

class Router:
    def __init__(self, name, interfaces, routes):
        """
        interfaces: list of IPv4 addresses (strings) assigned to the router
        routes: list of dicts: { "dest": "10.0.0.0/8", "next_hop": "10.0.0.1", "interface": "eth0" }
        """
        self.name = name
        self.interfaces = interfaces
        # Pre-parse networks for quicker comparisons
        self.routes = []
        for r in routes:
            rcopy = r.copy()
            rcopy["network"] = ipaddress.ip_network(r["dest"])
            self.routes.append(rcopy)

    def longest_prefix_match(self, dst_ip):
        ip = ipaddress.ip_address(dst_ip)
        best = None
        best_pref = -1
        for r in self.routes:
            if ip in r["network"]:
                prefix_len = r["network"].prefixlen
                if prefix_len > best_pref:
                    best = r
                    best_pref = prefix_len
        return best

    def is_connected_to(self, host_ip):
        """
        For simplicity: check /24 network membership with any interface
        """
        host = ipaddress.ip_address(host_ip)
        for iface in self.interfaces:
            try:
                iface_net = ipaddress.ip_network(iface + "/24", strict=False)
                if host in iface_net:
                    return True
            except Exception:
                pass
        return False


class RouterEngine:
    def __init__(self, routers_config):
        """
        routers_config: dict name -> { "interfaces": [...], "routes": [...] }
        """
        self.routers = {}
        for name, cfg in routers_config.items():
            self.routers[name] = Router(name, cfg.get("interfaces", []), cfg.get("routes", []))

    def find_router_for_host(self, host_ip):
        for r in self.routers.values():
            if r.is_connected_to(host_ip):
                return r
        return None

    def find_router_by_interface(self, ip_addr):
        for r in self.routers.values():
            for iface in r.interfaces:
                if iface == ip_addr:
                    return r
        return None
