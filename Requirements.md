This project is about demonstrating the use of claude to build an AVD design to support building and deploying a simple ST2110 network.

I want you to be an AVD (avd.arista.com) expert

We will keep the design info in github
We will aim to deply to arista ACT (arista cloud test).
For ACT, we'll need an inventory file, and then we'll need to push configs to on-prem CVP.

We'll build two simple networks, one red, one blue.
Each has 2 spines, and 4 leafs.
Each runs BGP in the underlay
Each runs PTPv2 with AES-R16 timing.
Infrastructure IPs are in the range 10.0.0.0/24. /31 can be used.
Management addresses are in the range 192.168.0.0/24, with gateway at 192.168.0.1

Switch types are 7280cr3a-48YC8 for leafs
7280CR3A-32S for spines.

host names would be
red_spine1
red_spine2
red_leaf1 etc.

install arista's avd (avd.arista.com) if needed
Please add info to this doc as we make decisions, emabling you to pick up at any point
When we push to giyhub, we'll push to this project: https://github.com/GerardPhillips/SMPTE_Bootcamp_Demo

## Decisions Made

### Current Topology (scaled down for demo)
- Red: 1 spine (red-spine1) + 3 leafs (red-leaf1..3)
- Blue: 1 spine (blue-spine1) + 3 leafs (blue-leaf1..3)
- PTP: 2 distribution switches (ptp-leaf-1, ptp-leaf-2) + 2 GMs
- Total: 10 switches

### Hostnames
Hyphens (AVD convention): red-spine1, red-leaf1..3, blue-spine1, blue-leaf1..3

### Switch Models
- Spines: 7280CR3A-32S
- Red/Blue leafs: 7280SR3-48YC8
- PTP distribution: 720XP-48Y6

### PTP Distribution Tier
- Two PTP distribution switches, each uplinked to both spines (25G)
- Two GMs: GM1 on ptp-leaf-1 Eth48, GM2 on ptp-leaf-2 Eth48, VLAN 2222
- Peer links between PTP leafs on Eth46/47 (25G) for BMCA
- PTP profile: aes67-r16-2016, domain 127
- Priority1: PTP leafs=10, Spines=20, Leafs=30

### No EVPN/VXLAN
Pure L2/L3 design with overlay_routing_protocol: none. Custom node types disable VTEP.

### IP Addressing (10.0.0.0/24)
- Loopback pool: 10.0.0.0/24 (shared, offsets prevent overlap)
  - Red spine: offset 0 (10.0.0.1)
  - Red leafs: offset 10 (10.0.0.11-13)
  - Blue spine: offset 50 (10.0.0.51)
  - Blue leafs: offset 60 (10.0.0.61-63)
  - PTP leafs: offset 80 (10.0.0.81-82)
- Red P2P uplinks: 10.0.0.128/26
- PTP P2P uplinks: 10.0.0.160/27
- Blue P2P uplinks: 10.0.0.192/26
- PTP peer links: 10.0.0.240-243/31

### Management (192.168.0.0/24, gw .1)
- red-spine1: .11, red-leaf1..3: .13-.15
- blue-spine1: .21, blue-leaf1..3: .23-.25
- ptp-leaf-1/2: .31/.32

### BGP AS (eBGP underlay, multicast enabled)
- Red spine: 65101, Red leafs: 65111-65113
- Blue spine: 65201, Blue leafs: 65211-65213
- PTP leafs: 65301-65302

### Multicast (PIM Sparse Mode)
- Red RP: 10.0.0.1 (red-spine1), Blue RP: 10.0.0.51 (blue-spine1)

### Interface Mapping
- Spines (7280CR3A-32S): Eth1-3 to fabric leafs, Eth4-5 to PTP leafs
- Leafs (7280SR3-48YC8): Eth49 uplink to spine1
- PTP leafs (720XP-48Y6): Eth1-2 (25G) uplinks to spines, Eth46-47 peer links

### CVP Deployment
- CVP address: 10.18.129.180
- TerminAttr streaming to 10.18.129.180:9910
- Token from cvaas_user_token file
- Configlet naming: AVD-${hostname}

### CloudVision Tags
- All devices: Campus=DC1, Campus-Pod=Pod1, dc=SMPTE-Bootcamp
- Spines: Role=Spine
- Leafs: Role=Leaf, Access-Pod=Red-Rack1/2/3 or Blue-Rack1/2/3
- PTP leafs: Role=PTP-Distribution
- Auto-generated topology hints: fabric, pod, type, rack

### Toolchain (already installed)
- ansible-core 2.16.3, arista.avd 6.2.0, arista.cvp 3.10.1, Python 3.10.4

-- Don't change this section without asking, i need to keep thoughts about the demo.
1/ Read the requirements.md file and do some planning