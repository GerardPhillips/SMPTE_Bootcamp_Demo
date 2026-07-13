# FABRIC

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| Blue | l3leaf | blue-leaf1 | 192.168.0.23/24 | 7280SR3-48YC8 | Provisioned | - |
| Blue | l3leaf | blue-leaf2 | 192.168.0.24/24 | 7280SR3-48YC8 | Provisioned | - |
| Blue | l3leaf | blue-leaf3 | 192.168.0.25/24 | 7280SR3-48YC8 | Provisioned | - |
| Blue | spine | blue-spine1 | 192.168.0.21/24 | 7280CR3A-32S | Provisioned | - |
| PTP | ptpleaf | ptp-leaf-1 | 192.168.0.31/24 | 720XP-48Y6 | Provisioned | - |
| PTP | ptpleaf | ptp-leaf-2 | 192.168.0.32/24 | 720XP-48Y6 | Provisioned | - |
| Red | l3leaf | red-leaf1 | 192.168.0.13/24 | 7280SR3-48YC8 | Provisioned | - |
| Red | l3leaf | red-leaf2 | 192.168.0.14/24 | 7280SR3-48YC8 | Provisioned | - |
| Red | l3leaf | red-leaf3 | 192.168.0.15/24 | 7280SR3-48YC8 | Provisioned | - |
| Red | spine | red-spine1 | 192.168.0.11/24 | 7280CR3A-32S | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | --------- | -------------- |
| l3leaf | blue-leaf1 | Ethernet49/1 | spine | blue-spine1 | Ethernet1/1 |
| l3leaf | blue-leaf2 | Ethernet49/1 | spine | blue-spine1 | Ethernet2/1 |
| l3leaf | blue-leaf3 | Ethernet49/1 | spine | blue-spine1 | Ethernet3/1 |
| spine | blue-spine1 | Ethernet4/1 | ptpleaf | ptp-leaf-1 | Ethernet2 |
| spine | blue-spine1 | Ethernet5/1 | ptpleaf | ptp-leaf-2 | Ethernet2 |
| ptpleaf | ptp-leaf-1 | Ethernet1 | spine | red-spine1 | Ethernet4/1 |
| ptpleaf | ptp-leaf-1 | Ethernet46 | ptpleaf | ptp-leaf-2 | Ethernet46 |
| ptpleaf | ptp-leaf-1 | Ethernet47 | ptpleaf | ptp-leaf-2 | Ethernet47 |
| ptpleaf | ptp-leaf-2 | Ethernet1 | spine | red-spine1 | Ethernet5/1 |
| l3leaf | red-leaf1 | Ethernet49/1 | spine | red-spine1 | Ethernet1/1 |
| l3leaf | red-leaf2 | Ethernet49/1 | spine | red-spine1 | Ethernet2/1 |
| l3leaf | red-leaf3 | Ethernet49/1 | spine | red-spine1 | Ethernet3/1 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 10.0.0.128/26 | 64 | 14 | 21.88 % |
| 10.0.0.160/27 | 32 | 8 | 25.0 % |
| 10.0.0.192/26 | 64 | 10 | 15.63 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| blue-leaf1 | Ethernet49/1 | 10.0.0.193/31 | blue-spine1 | Ethernet1/1 | 10.0.0.192/31 |
| blue-leaf2 | Ethernet49/1 | 10.0.0.195/31 | blue-spine1 | Ethernet2/1 | 10.0.0.194/31 |
| blue-leaf3 | Ethernet49/1 | 10.0.0.197/31 | blue-spine1 | Ethernet3/1 | 10.0.0.196/31 |
| blue-spine1 | Ethernet4/1 | 10.0.0.162/31 | ptp-leaf-1 | Ethernet2 | 10.0.0.163/31 |
| blue-spine1 | Ethernet5/1 | 10.0.0.166/31 | ptp-leaf-2 | Ethernet2 | 10.0.0.167/31 |
| ptp-leaf-1 | Ethernet1 | 10.0.0.161/31 | red-spine1 | Ethernet4/1 | 10.0.0.160/31 |
| ptp-leaf-1 | Ethernet46 | 10.0.0.242/31 | ptp-leaf-2 | Ethernet46 | 10.0.0.243/31 |
| ptp-leaf-1 | Ethernet47 | 10.0.0.240/31 | ptp-leaf-2 | Ethernet47 | 10.0.0.241/31 |
| ptp-leaf-2 | Ethernet1 | 10.0.0.165/31 | red-spine1 | Ethernet5/1 | 10.0.0.164/31 |
| red-leaf1 | Ethernet49/1 | 10.0.0.129/31 | red-spine1 | Ethernet1/1 | 10.0.0.128/31 |
| red-leaf2 | Ethernet49/1 | 10.0.0.131/31 | red-spine1 | Ethernet2/1 | 10.0.0.130/31 |
| red-leaf3 | Ethernet49/1 | 10.0.0.133/31 | red-spine1 | Ethernet3/1 | 10.0.0.132/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 10.0.0.0/24 | 256 | 10 | 3.91 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| Blue | blue-leaf1 | 10.0.0.61/32 |
| Blue | blue-leaf2 | 10.0.0.62/32 |
| Blue | blue-leaf3 | 10.0.0.63/32 |
| Blue | blue-spine1 | 10.0.0.51/32 |
| PTP | ptp-leaf-1 | 10.0.0.81/32 |
| PTP | ptp-leaf-2 | 10.0.0.82/32 |
| Red | red-leaf1 | 10.0.0.11/32 |
| Red | red-leaf2 | 10.0.0.12/32 |
| Red | red-leaf3 | 10.0.0.13/32 |
| Red | red-spine1 | 10.0.0.1/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
