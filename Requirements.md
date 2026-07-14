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
- Spines (7280CR3A-32S): Eth1/1-3/1 to fabric leafs, Eth4/1-5/1 to PTP leafs
- Leafs (7280SR3-48YC8): Eth49/1 uplink to spine1
- PTP leafs (720XP-48Y6): Eth1-2 (25G) uplinks to spines, Eth46-47 peer links

### Example Host Ports (on red-leaf1 and blue-leaf1, symmetric)
- **Ethernet1 — Routed port (L3 host)**
  - No switchport, /31 point-to-point IP
  - PIM sparse-mode + PTP enabled (role master)
  - red-leaf1: 10.10.101.0/31, blue-leaf1: 10.10.201.0/31
- **Ethernet2 — Access switchport (L2 host)**
  - VLAN 100 (Red-Media) / VLAN 200 (Blue-Media)
  - PTP enabled (role master)
  - SVI gateway: red-leaf1 Vlan100 10.10.100.1/24, blue-leaf1 Vlan200 10.10.200.1/24
- Host configs defined via structured_config (routed) and media_hosts.yml (switchport)
- Spines excluded from NETWORK_SERVICES to prevent VLAN leaking

### CVP Deployment
- CVP address: 10.18.129.180 (external), 192.168.0.5 (internal/TerminAttr)
- TerminAttr streaming to 192.168.0.5:9910
- Token from cvaas_user_token file
- Configlet naming: AVD-${hostname}

### CloudVision Tags
- All devices: Campus=DC1, Campus-Pod=Pod1, dc=SMPTE-Bootcamp
- Spines: Role=Spine, topology_hint_type=spine
- Leafs: Role=Leaf, Access-Pod=Red-Rack1/2/3 or Blue-Rack1/2/3, topology_hint_type=leaf
- PTP leafs: Role=PTP-Distribution, topology_hint_type=superspine (renders above pods in CVaaS topology view)
- PTP leafs have topology_hints disabled (no auto pod/rack tags) to float above Red/Blue pods
- Auto-generated topology hints for all other devices: fabric, pod, type, rack

### Toolchain (already installed)
- ansible-core 2.16.3, arista.avd 6.2.0, arista.cvp 3.10.1, Python 3.10.4

## Improvements

### Critical

1. ~~**PTP Clock Identity Collision**~~ **RESOLVED** — Blue fabric nodes now have unique clock identities (byte 4: 00=Red, 01=Blue) via structured_config overrides.

2. **Plaintext Credentials in Inventory** — `ansible_password: arista123!` is in `inventory.yml` in cleartext. Should use Ansible Vault or environment variables before any public push.

3. **HTTP Enabled on eAPI** — `enable_http: true` in FABRIC.yml allows unencrypted management access. Set to `false` for production.

4. **PTP Leafs Missing PIM RP** — ptp-leaf-1/2 have PIM sparse-mode on uplinks but no RP address configured. Multicast traversing the PTP tier will fail. Add RP config to PTP.yml.

5. **Overlapping IP Pools (Latent)** — Red P2P pool (10.0.0.128/26) overlaps with PTP P2P pool (10.0.0.160/27). No collision today with 3 leafs, but scaling Red beyond ~16 leafs would conflict. Shrink Red pool to /27.

### Recommended

6. **BFD on BGP Peers** — No BFD configured; BGP failover takes up to 180s. ST2110 needs sub-second convergence. Add `bfd: true` to BGP peer groups.

7. **Jumbo MTU on Host Ports** — Routed port (Eth1) and switchport (Eth2) on leafs have no MTU set (defaults to 1500). ST2110 video requires jumbo frames (9214).

8. **Management VRF Separation** — Management is in VRF `default`, sharing the data plane. Use a dedicated `MGMT` VRF for management plane isolation.

9. **BGP Route Filtering** — `redistribute connected` has no route-map filter. Could leak unintended prefixes. Add prefix-list and route-map.

10. **NTP Redundancy** — Only one NTP server configured. Best practice is minimum 3 sources for falseticker detection.

11. **Logging / Syslog** — No syslog configuration. Add buffered logging and remote syslog server for PTP events, multicast state changes, and interface flaps.

12. **SNMP** — No SNMP configured. Needed for monitoring PTP metrics, interface counters, multicast state.

13. **Spanning-Tree** — No explicit STP mode or root priority. Should configure MSTP with defined root bridges to prevent L2 loops.

14. **Storm Control on Access Ports** — No storm-control on media host ports. A broadcast storm could disrupt PTP and media flows.

15. **AAA / TACACS+** — Only local authentication. Production should add centralized AAA with local fallback.

16. **Login Banner** — No banner configured. Often a compliance requirement.

17. **QoS / DSCP for ST2110** — No QoS policies defined. ST2110 requires traffic classification: PTP (DSCP 46/48), media essence (DSCP 34), metadata (DSCP 26).

18. **IGMP Snooping / Fast-Leave** — Not explicitly configured on media VLANs. Enable fast-leave on single-host access ports for minimal multicast leave latency.

19. **Control-Plane Policing (CoPP)** — No CoPP configured. Switch CPU vulnerable to excessive control-plane traffic.

20. **LLDP Explicit Config** — EOS enables LLDP by default, but ST2110/NMOS environments benefit from explicit TLV and management address configuration.

21. **PIM RP Redundancy** — Single RP per fabric on the single spine. When scaling to 2 spines, add Anycast RP.

22. **PTP VLAN Gateway Redundancy** — VLAN 2222 has two SVI IPs but no VRRP/VARP. GMs lose connectivity if their specific PTP leaf fails.

23. ~~**sFlow Not Generating**~~ **RESOLVED** — Now uses `sflow_settings.export_to_cloudvision.enabled: true`, auto-configured via TerminAttr.

24. ~~**`build.yml` Deprecated `collections` Keyword**~~ **RESOLVED** — Removed `collections:` block, tasks now use FQCNs exclusively.

### Anti-Patterns Resolved (from AVD schema compliance review)
- DNS config now uses native `dns_settings` instead of `custom_structured_configuration_ip_name_server`
- sFlow now uses `sflow_settings.export_to_cloudvision` instead of hardcoded 127.0.0.1 destination
- `build.yml` uses FQCNs exclusively, deprecated `collections:` block removed
- `deploy.yml` documents external vs internal CVP address difference

### Nice-to-Have

25. **FEC on High-Speed Interfaces** — No explicit error-correction encoding. Consider RS-FEC for 25G, CL91 for 100G to prevent interop issues.

26. **errdisable Recovery** — No auto-recovery configured. Ports stuck in errdisable require manual intervention.

27. **`ansible_python_interpreter: $(which python3)`** — Shell expansion may not work in all Ansible execution contexts (AWX/Tower). Use an explicit path.

28. **virtualDCS.yml Plaintext Passwords** — Lab passwords in cleartext committed to repo.

-- Don't change this section without asking, i need to keep thoughts about the demo.
1/ Read the requirements.md file and do some planning