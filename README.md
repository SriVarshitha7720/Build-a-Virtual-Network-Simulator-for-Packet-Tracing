# Packet Tracer API Simulator
This project implements an API-driven simulator that traces the journey of a network packet through a configurable virtual network. It models fundamental networking concepts, including DNS resolution (A and CNAME records), Longest Prefix Match (LPM) routing, Time-to-Live (TTL) decrementing, and ordered firewall rule processing.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7f7d04e3-7e01-4f44-a4c1-1f1fc1bdfb34" />
# Network Packet Tracer Simulator
This project implements a functional, modular simulator designed to trace the path of a network packet through a customizable, multi-device topology. Built using Python and Flask, the simulator provides a comprehensive, step-by-step trace output (JSON) that demonstrates core networking concepts.


**Core Technical Features Demonstrated**


-> This simulator proves compliance with essential networking requirements:

-> **Routing Engine**:Implements the Longest Prefix Match (LPM) algorithm for accurate route selection across multiple configured routers.

-> **Security Enforcement:** Features an Ordered Firewall Engine supporting contextual DENY/ALLOW actions, port ranges, and enforcing the Implicit Deny policy.

-> **DNS Resolution:** Handles both A (Address) records and recursive resolution of CNAME (Canonical Name) aliases.

-> **Packet Lifecycle:** Correctly decrements Time-To-Live (TTL) at each hop.

-> **Topology:** Uses a modular architecture with dynamic configuration loaded from config/ files, supporting complex multi-hop paths.
