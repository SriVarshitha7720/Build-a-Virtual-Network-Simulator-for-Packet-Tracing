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

# ⚙️ Setup and Installation
Follow these steps to set up and run the simulator:

**1. Clone the Repository**:

Bash :

>>> git clone https://github.com/SriVarshitha7720/Build-a-Virtual-Network-Simulator-for-Packet-Tracing
>>> cd packet-tracer-simulator

**2.Install Dependencies**:

Bash :

**Install Flask and other required libraries**
>>> pip install -r requirements.txt

**3.Run the Application**:

Bash :

#Start the Flask development server
>>> flask run --host=0.0.0.0 --port=5000

The server will start running on http://127.0.0.1:5000

![WhatsApp Image 2025-12-11 at 22 15 22_7187876b](https://github.com/user-attachments/assets/8196c2eb-bb56-43b0-97bd-0274d51ab9e3)


# 🧪 API Documentation: The /trace Endpoint
The simulation is executed via a single HTTP POST endpoint.

**Endpoint Details**
**Method**: POST

**URL**: http://127.0.0.1:5000/trace

**Request Payload (application/json)**
The request must contain all 5 fields as defined in the app.py validation.

**Example Scenario A**: Successful Multi-Hop Trace
This trace uses scenario-complex.json to demonstrate CNAME resolution, multi-hop LPM, and Firewall ALLOW.

**Input Payload (test_full_trace.json)**:
Code :


{
    
    "src_ip": "192.168.100.50",
    "dst": "www.example.com",
    "dst_port": 80,
    "protocol": "TCP",
    "ttl": 5
}

Key Trace Events (Verification):

![WhatsApp Image 2025-12-11 at 21 55 01_4e1201ee](https://github.com/user-attachments/assets/54f8f15c-3a36-4e32-b51b-be2a48d88641)

**Example Scenario B:** Failed Trace (Firewall Block)
This trace uses scenario-complex.json to demonstrate ordered firewall processing and immediate termination.

**Input Payload (test_full_block.json):**

Code :

{

    "src_ip": "192.168.100.10",
    "dst": "api.internal",
    "dst_port": 8500,  
    "protocol": "TCP",
    "ttl": 5
}

**Key Trace Events (Verification):**


JSON 

// ... DNS resolution successful: api.internal resolved to 10.10.0.50
// ... R1 (Edge) Firewall check: Matched rule #2 (DENY) on router Edge
// ... Final Status: Packet blocked by firewall on Edge


**Verification** : The packet was correctly blocked by Rule #2 (which targets port range 8000-9000 from the source subnet 192.168.100.x), proving that the ordered rules take precedence over the final ALLOW rule.
