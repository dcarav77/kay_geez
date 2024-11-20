# Import necessary libraries
import matplotlib.pyplot as plt
import networkx as nx

# Initialize the knowledge graph
G_hpt = nx.DiGraph()

# Define categories
categories_hpt = [
    "Engine", "Part", "Fault", "Maintenance Action", "Cost", "Event"
]

# Define realistic engines
engines = [
    "Rolls-Royce BR700-715A1-30", 
    "Rolls-Royce BR700-715B1-30", 
    "Rolls-Royce BR700-715C1-30", 
    "CL-600-2B19 Series", 
    "General Electric CF34-8C5B1",
    "Pratt & Whitney PW1500G"
]

# Define realistic HPT parts
parts_hpt = [
    "HPT Stage 1 Disk", "HPT Stage 2 Disk", "HPT Torque Shaft", 
    "HPT Interstage Seal Disk", "HPT Blades (Stage 1)", "HPT Blades (Stage 2)", 
    "HPT Front Cover Plate", "HPT Rear Cover Plate", "HPT Curvic Ring", 
    "HPT Bolting (Stage 1 & 2)", "Inducer Seal", "Interstage Seal", 
    "Turbine Aft Seal Disk", "CDP Seal", "Oil Seal (High-Pressure)", 
    "Air Seal (High-Pressure)", "Shaft Seal", "NGV Seal", "Torque Shaft Cover", 
    "Stub Shaft", "LPT Main Shaft", "Stage 1 Disk", "Stage 2 Disk", 
    "Impeller Disk", "Turbine Shaft Coupling Disk", "NGV", 
    "HPT Cooling Vanes", "HPT Nozzle", "HPT Cooling Holes", 
    "HPT Cooling Channels", "HPT Casing", "High-Pressure Air Duct", 
    "HPT Retaining Ring", "HPT Locking Plates", "HPT Blade Shroud", 
    "HPT Disc Retention Bolts", "Turbine Wheel Hub", "High-Pressure Air Pipe", 
    "Gas Path Seals", "HPT Disk Spacer"
]


# Define realistic faults
faults_hpt = [
    "Braze Failure", "Tip Cap Loss", "Creep Deformation", 
    "Low Cycle Fatigue (LCF)", "High Cycle Fatigue (HCF)", 
    "Thermal Fatigue Cracking", "Stress Concentration Fracture", 
    "Blade/Disk Dovetail Cracking", "Vibratory Stress Failure", 
    "Overtemperature Induced Failure", "Seal Leakage", 
    "Disk Cracking", "Blade Tip Burnout", "Bolt Hole Fracture", 
    "Interstage Seal Erosion", "Tip Clearance Wear", 
    "Rotor Overspeed Damage", "Oxidation and Corrosion", 
    "Foreign Object Damage (FOD)", "HPT Blade Shear Failure"
]


# Define maintenance actions
actions_hpt = [
    "Replace HPT Disk", "Inspect Seal Integrity", "Recalibrate Torque Shaft",
    "Perform Weld Overlay on Blade Tip", "Re-coat Blade with Aluminide Coating",
    "Restore Dimensional Integrity of Blade", "Replace High-Pressure Turbine Blade",
    "Repair Vane Airfoil Cracks", "Restore Platform Dimensions", 
    "Replace Low-Pressure Turbine Blade", "Perform Metallurgical Crack Repair",
    "Re-coat Low-Pressure Turbine Blade", "Restore Tip Shroud", 
    "Inspect and Replace Airfoil Coatings", "Perform Crack Repair on Vane",
    "Inspect Blade Dovetail Integrity", "Replace Cooling Channels",
    "Repair Blade Platform Cracks", "Inspect and Repair Gas Path Seals",
    "Replace High-Pressure Air Pipe"
]

# Define costs
costs_hpt = [
    "$10,000", "$5,000", "$15,000", "$7,500", "$12,000"
]

# Add nodes for all categories
for engine in engines:
    G_hpt.add_node(engine, category="Engine")

for part in parts_hpt:
    G_hpt.add_node(part, category="Part")

for fault in faults_hpt:
    G_hpt.add_node(fault, category="Fault")

for action in actions_hpt:
    G_hpt.add_node(action, category="Maintenance Action")

for cost in costs_hpt:
    G_hpt.add_node(cost, category="Cost")

# Add relationships
# Engines -> Parts
for engine in engines:
    for _ in range(2):  # Connect each engine to 2 parts
        part = parts_hpt.pop(0) if parts_hpt else None
        if part:
            G_hpt.add_edge(engine, part, relationship="contains component")

# Parts -> Faults
for part in list(G_hpt.nodes):
    if G_hpt.nodes[part].get("category") == "Part":
        fault = faults_hpt.pop(0) if faults_hpt else None
        if fault:
            G_hpt.add_edge(part, fault, relationship="has fault")

# Faults -> Maintenance Actions
for fault in list(G_hpt.nodes):
    if G_hpt.nodes[fault].get("category") == "Fault":
        action = actions_hpt.pop(0) if actions_hpt else None
        if action:
            G_hpt.add_edge(fault, action, relationship="is addressed by")

# Faults -> Costs
for fault, cost in zip(faults_hpt, costs_hpt):
    G_hpt.add_edge(fault, cost, relationship="incurs cost")

# Add additional edges
additional_edges = [
    ("HPT Stage 1 Disk", "Low Cycle Fatigue (LCF)", "is prone to"),
    ("HPT Stage 2 Disk", "High Cycle Fatigue (HCF)", "is prone to"),
    ("HPT Blades (Stage 1)", "Blade Tip Burnout", "commonly experiences"),
    ("HPT Blades (Stage 2)", "Braze Failure", "commonly experiences"),
    ("HPT Interstage Seal Disk", "Seal Leakage", "can result in"),
    ("HPT Torque Shaft", "Rotor Overspeed Damage", "can lead to"),
    ("HPT Cooling Channels", "Overtemperature Induced Failure", "can cause"),
    ("HPT Locking Plates", "Stress Concentration Fracture", "is susceptible to"),
    ("HPT Casing", "Oxidation and Corrosion", "is vulnerable to"),
    ("Gas Path Seals", "Foreign Object Damage (FOD)", "is affected by")
]

for source, target, relationship in additional_edges:
    G_hpt.add_edge(source, target, relationship=relationship)

# Visualize the graph
plt.figure(figsize=(18, 14))

# Define positions for nodes
pos_hpt = nx.spring_layout(G_hpt, seed=42)

# Node colors based on categories
categories_hpt = list(set(nx.get_node_attributes(G_hpt, "category").values()))
colors_hpt = plt.cm.tab20(range(len(categories_hpt)))

# Ensure "Engine" nodes are green and "Cost" nodes are red
node_colors_hpt = [
    "green" if G_hpt.nodes[node]["category"] == "Engine" else
    "red" if G_hpt.nodes[node]["category"] == "Cost" else
    colors_hpt[categories_hpt.index(G_hpt.nodes[node]["category"])]
    for node in G_hpt.nodes()
]

# Draw nodes and edges
nx.draw_networkx_nodes(G_hpt, pos_hpt, node_color=node_colors_hpt, node_size=1200, alpha=0.9)
nx.draw_networkx_edges(G_hpt, pos_hpt, arrowstyle="->", arrowsize=10, edge_color="gray")
nx.draw_networkx_labels(G_hpt, pos_hpt, font_size=8, font_color="black", font_weight="bold")

# Add edge labels to show relationships
edge_labels = nx.get_edge_attributes(G_hpt, "relationship")
nx.draw_networkx_edge_labels(G_hpt, pos_hpt, edge_labels=edge_labels, font_size=8)

# Add legend
legend_elements_hpt = [
    plt.Line2D([0], [0], marker="o", color="w", label=category, markersize=10, 
               markerfacecolor=("green" if category == "Engine" else
                                "red" if category == "Cost" else
                                colors_hpt[i]))
    for i, category in enumerate(categories_hpt)
]
plt.legend(handles=legend_elements_hpt, loc="lower center", bbox_to_anchor=(0.5, -0.1), 
           title="Node Categories", ncol=3, frameon=False)

# Add title to the graph
plt.title("Knowledge Graph of HPT Parts, Faults, Maintenance Actions, and Costs", fontsize=16)

# Remove axes for better visualization
plt.axis("off")

# Show the graph
plt.show()
