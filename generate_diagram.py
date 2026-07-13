import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(22, 18))
ax.set_xlim(-1, 23)
ax.set_ylim(-2.5, 17)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#1a1a2e')

COLORS = {
    'red_spine': '#c0392b',
    'red_leaf': '#e74c3c',
    'blue_spine': '#2471a3',
    'blue_leaf': '#3498db',
    'ptp': '#8e44ad',
    'gm': '#27ae60',
    'text': '#ecf0f1',
    'link': '#7f8c8d',
    'ptp_link': '#9b59b6',
    'border_red': '#e74c3c',
    'border_blue': '#3498db',
}

def draw_switch(ax, x, y, label, sublabel, color, width=2.2, height=0.9):
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.1", facecolor=color,
                          edgecolor='white', linewidth=1.5, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y + 0.12, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color='white', family='monospace')
    ax.text(x, y - 0.2, sublabel, ha='center', va='center',
            fontsize=6.5, color='#d5d8dc', family='monospace')

def draw_link(ax, x1, y1, x2, y2, color='#7f8c8d', lw=1.0, style='-'):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, linestyle=style,
            alpha=0.6, zorder=1)

# Title
ax.text(11, 16.2, 'SMPTE Bootcamp Demo — Physical Topology',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color='white', family='sans-serif')
ax.text(11, 15.6, 'Dual ST2110 Fabric with PTP Distribution',
        ha='center', va='center', fontsize=11, color='#aab7b8', family='sans-serif')

# --- GMs ---
gm1_x, gm1_y = 9, 14.2
gm2_x, gm2_y = 13, 14.2
draw_switch(ax, gm1_x, gm1_y, 'PTP GM 1', 'Eth48 → ptp-leaf-1', COLORS['gm'], width=2.4)
draw_switch(ax, gm2_x, gm2_y, 'PTP GM 2', 'Eth48 → ptp-leaf-2', COLORS['gm'], width=2.4)

# --- PTP Tier (y=12) ---
ptp_y = 12.2
ptp1_x, ptp2_x = 9, 13
draw_switch(ax, ptp1_x, ptp_y, 'ptp-leaf-1', '720XP-48Y6  192.168.0.31', COLORS['ptp'], width=2.8)
draw_switch(ax, ptp2_x, ptp_y, 'ptp-leaf-2', '720XP-48Y6  192.168.0.32', COLORS['ptp'], width=2.8)

# GM to PTP leaf links
draw_link(ax, gm1_x, gm1_y - 0.45, ptp1_x, ptp_y + 0.45, color=COLORS['gm'], lw=2)
draw_link(ax, gm2_x, gm2_y - 0.45, ptp2_x, ptp_y + 0.45, color=COLORS['gm'], lw=2)

# PTP peer links
draw_link(ax, ptp1_x + 1.4, ptp_y + 0.1, ptp2_x - 1.4, ptp_y + 0.1, color=COLORS['gm'], lw=1.8)
draw_link(ax, ptp1_x + 1.4, ptp_y - 0.1, ptp2_x - 1.4, ptp_y - 0.1, color=COLORS['gm'], lw=1.8)
ax.text(11, ptp_y + 0.35, 'Eth46,47 25G (PTP/BMCA)', ha='center', va='center',
        fontsize=6, color='#27ae60', family='monospace')

# --- Spine Tier (y=9.5) ---
spine_y = 9.5
red_spine_x = 4.5
blue_spine_x = 17.5
draw_switch(ax, red_spine_x, spine_y, 'red-spine1',
            '7280CR3A-32S  192.168.0.11  AS 65101', COLORS['red_spine'], width=2.8)
draw_switch(ax, blue_spine_x, spine_y, 'blue-spine1',
            '7280CR3A-32S  192.168.0.21  AS 65201', COLORS['blue_spine'], width=2.8)

# PTP to spine links
for px in [ptp1_x, ptp2_x]:
    for sx in [red_spine_x, blue_spine_x]:
        draw_link(ax, px, ptp_y - 0.45, sx, spine_y + 0.45,
                  color=COLORS['ptp_link'], lw=1.2, style='--')

# --- Leaf Tier (y=6.5) ---
leaf_y = 6.5
red_leaf_positions = {
    'red-leaf1': (2, leaf_y),
    'red-leaf2': (4.5, leaf_y),
    'red-leaf3': (7, leaf_y),
}
blue_leaf_positions = {
    'blue-leaf1': (15, leaf_y),
    'blue-leaf2': (17.5, leaf_y),
    'blue-leaf3': (20, leaf_y),
}
red_leaf_info = {
    'red-leaf1': ('192.168.0.13', 'AS 65111'),
    'red-leaf2': ('192.168.0.14', 'AS 65112'),
    'red-leaf3': ('192.168.0.15', 'AS 65113'),
}
blue_leaf_info = {
    'blue-leaf1': ('192.168.0.23', 'AS 65211'),
    'blue-leaf2': ('192.168.0.24', 'AS 65212'),
    'blue-leaf3': ('192.168.0.25', 'AS 65213'),
}

for name, (x, y) in red_leaf_positions.items():
    ip, asn = red_leaf_info[name]
    draw_switch(ax, x, y, name, f'SR3-48YC8  {ip}  {asn}', COLORS['red_leaf'], width=2.4)

for name, (x, y) in blue_leaf_positions.items():
    ip, asn = blue_leaf_info[name]
    draw_switch(ax, x, y, name, f'SR3-48YC8  {ip}  {asn}', COLORS['blue_leaf'], width=2.4)

# Red leaf to red-spine1 links
for lname, (lx, ly) in red_leaf_positions.items():
    draw_link(ax, lx, ly + 0.45, red_spine_x, spine_y - 0.45,
              color=COLORS['border_red'], lw=1.0)

# Blue leaf to blue-spine1 links
for lname, (lx, ly) in blue_leaf_positions.items():
    draw_link(ax, lx, ly + 0.45, blue_spine_x, spine_y - 0.45,
              color=COLORS['border_blue'], lw=1.0)

# --- Host devices below leaf1s ---
host_y = 4.5
host_color = '#566573'

# Red hosts
draw_switch(ax, 1, host_y, 'L3 Host', 'Eth1 routed  10.10.101.1/31', host_color, width=2.2, height=0.7)
draw_switch(ax, 3.2, host_y, 'L2 Host', 'Eth2 VLAN 100  10.10.100.x/24', host_color, width=2.2, height=0.7)
draw_link(ax, 1, host_y + 0.35, 2, leaf_y - 0.45, color='#f39c12', lw=1.5)
draw_link(ax, 3.2, host_y + 0.35, 2, leaf_y - 0.45, color='#f39c12', lw=1.5)
ax.text(0.6, host_y + 0.55, 'PIM+PTP', ha='center', va='center', fontsize=5.5, color='#f39c12', family='monospace')
ax.text(3.6, host_y + 0.55, 'PTP', ha='center', va='center', fontsize=5.5, color='#f39c12', family='monospace')

# Blue hosts
draw_switch(ax, 14, host_y, 'L3 Host', 'Eth1 routed  10.10.201.1/31', host_color, width=2.2, height=0.7)
draw_switch(ax, 16.2, host_y, 'L2 Host', 'Eth2 VLAN 200  10.10.200.x/24', host_color, width=2.2, height=0.7)
draw_link(ax, 14, host_y + 0.35, 15, leaf_y - 0.45, color='#f39c12', lw=1.5)
draw_link(ax, 16.2, host_y + 0.35, 15, leaf_y - 0.45, color='#f39c12', lw=1.5)
ax.text(13.6, host_y + 0.55, 'PIM+PTP', ha='center', va='center', fontsize=5.5, color='#f39c12', family='monospace')
ax.text(16.6, host_y + 0.55, 'PTP', ha='center', va='center', fontsize=5.5, color='#f39c12', family='monospace')

# --- Fabric boundary boxes ---
red_box = FancyBboxPatch((0.5, 3.8), 8, 7.0, boxstyle="round,pad=0.3",
                          facecolor='none', edgecolor=COLORS['border_red'],
                          linewidth=2, linestyle='--', alpha=0.5)
ax.add_patch(red_box)
ax.text(4.5, 4.05, 'RED FABRIC', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLORS['border_red'],
        family='sans-serif', alpha=0.7)

blue_box = FancyBboxPatch((13.5, 3.8), 8, 7.0, boxstyle="round,pad=0.3",
                           facecolor='none', edgecolor=COLORS['border_blue'],
                           linewidth=2, linestyle='--', alpha=0.5)
ax.add_patch(blue_box)
ax.text(17.5, 4.05, 'BLUE FABRIC', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLORS['border_blue'],
        family='sans-serif', alpha=0.7)

ptp_box = FancyBboxPatch((7, 11.2), 8, 1.9, boxstyle="round,pad=0.3",
                          facecolor='none', edgecolor=COLORS['ptp'],
                          linewidth=2, linestyle='--', alpha=0.5)
ax.add_patch(ptp_box)
ax.text(11, 11.45, 'PTP DISTRIBUTION', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLORS['ptp'],
        family='sans-serif', alpha=0.7)

# --- Info box ---
info_items = [
    ('Underlay:', 'eBGP  |  PIM Sparse-Mode Multicast'),
    ('PTP:', 'AES67-R16  |  Domain 127  |  Boundary Clock'),
    ('Overlay:', 'None (pure L2/L3 for ST2110)'),
    ('Infra IPs:', '10.0.0.0/24  |  P2P /31s'),
    ('Mgmt:', '192.168.0.0/24  |  GW 192.168.0.1'),
    ('Red RP:', '10.0.0.1 (red-spine1)  |  Blue RP: 10.0.0.51 (blue-spine1)'),
]
info_box = FancyBboxPatch((3, -2.0), 16, 3.7, boxstyle="round,pad=0.2",
                           facecolor='#16213e', edgecolor='#34495e',
                           linewidth=1.5, alpha=0.8)
ax.add_patch(info_box)
for i, (key, val) in enumerate(info_items):
    ypos = 1.2 - i * 0.5
    ax.text(4, ypos, key, ha='left', va='center', fontsize=8.5,
            fontweight='bold', color='#f39c12', family='monospace')
    ax.text(7.5, ypos, val, ha='left', va='center', fontsize=8.5,
            color='#d5d8dc', family='monospace')

# --- Legend ---
legend_items = [
    (COLORS['red_spine'], 'Red Spine (7280CR3A-32S)'),
    (COLORS['red_leaf'], 'Red Leaf (7280SR3-48YC8)'),
    (COLORS['blue_spine'], 'Blue Spine (7280CR3A-32S)'),
    (COLORS['blue_leaf'], 'Blue Leaf (7280SR3-48YC8)'),
    (COLORS['ptp'], 'PTP Distribution (720XP-48Y6)'),
    (COLORS['gm'], 'PTP Grandmaster'),
    ('#566573', 'Media Host (example)'),
]
for i, (color, label) in enumerate(legend_items):
    lx = 0.2
    ly = 2.5 - i * 0.4
    ax.add_patch(FancyBboxPatch((lx, ly - 0.12), 0.3, 0.24,
                                 boxstyle="round,pad=0.02", facecolor=color,
                                 edgecolor='white', linewidth=0.5))
    ax.text(lx + 0.5, ly, label, ha='left', va='center', fontsize=7.5,
            color='#d5d8dc', family='sans-serif')

# Interface labels on spines
ax.text(red_spine_x, spine_y - 0.7, 'Eth1-3↓  Eth4-5→PTP', ha='center', va='center',
        fontsize=6, color='#95a5a6', family='monospace')
ax.text(blue_spine_x, spine_y - 0.7, 'Eth1-3↓  Eth4-5→PTP', ha='center', va='center',
        fontsize=6, color='#95a5a6', family='monospace')

# Interface labels on PTP leafs
ax.text(ptp1_x, ptp_y - 0.7, 'Eth1-2↓ 25G to spines', ha='center', va='center',
        fontsize=6, color='#95a5a6', family='monospace')
ax.text(ptp2_x, ptp_y - 0.7, 'Eth1-2↓ 25G to spines', ha='center', va='center',
        fontsize=6, color='#95a5a6', family='monospace')

plt.tight_layout(pad=0.5)
plt.savefig('/Users/gp/Documents/AVD/SMPTE_Bootcamp_Demo/SMPTE_Bootcamp_Topology.png',
            dpi=200, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Diagram saved.")
