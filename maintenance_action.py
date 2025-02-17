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

# Add nodes for engines, parts, faults, actions, and costs
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
from itertools import cycle

for engine in engines:
    for _ in range(2):
        if parts_hpt:  # Prevent list exhaustion
            part = parts_hpt.pop(0)
            G_hpt.add_edge(engine, part, relationship="contains component")

parts_cycle = cycle(parts_hpt)
for engine in engines:
    for _ in range(2):  # Connect each engine to 2 parts
        part = next(parts_cycle)
        G_hpt.add_edge(engine, part, relationship="contains component")

# Parts -> Faults
faults_cycle = cycle(faults_hpt)
for part in parts_hpt:
    fault = next(faults_cycle)
    G_hpt.add_edge(part, fault, relationship="has fault")

# Faults -> Maintenance Actions
actions_cycle = cycle(actions_hpt)
for fault in faults_hpt:
    action = next(actions_cycle)
    G_hpt.add_edge(fault, action, relationship="is addressed by")

# Faults -> Costs
costs_cycle = cycle(costs_hpt)
for fault in faults_hpt:
    cost = next(costs_cycle)
    G_hpt.add_edge(fault, cost, relationship="incurs cost")

# Add additional edges for specific relationships
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
node_colors_hpt = [
    "#5D3FD3" if G_hpt.nodes[node]["category"] == "Engine" else  # Dark purple for Engine
    "#FA8072" if G_hpt.nodes[node]["category"] == "Cost" else  # Salmon for Cost
    "#FFD700" if G_hpt.nodes[node]["category"] == "Fault" else  # Yellow for Fault
    "#32CD32" if G_hpt.nodes[node]["category"] == "Part" else  # Lime green for Part
    "#ADD8E6" if G_hpt.nodes[node]["category"] == "Maintenance Action" else  # Light blue for Maintenance Action
    "gray"  # Default fallback color
    for node in G_hpt.nodes()
]

# Draw nodes and edges
nx.draw_networkx_nodes(G_hpt, pos_hpt, node_color=node_colors_hpt, node_size=1200, alpha=0.9)
nx.draw_networkx_edges(G_hpt, pos_hpt, arrowstyle="->", arrowsize=10, edge_color="gray")
nx.draw_networkx_labels(G_hpt, pos_hpt, font_size=8, font_color="black", font_weight="bold")

# Add edge labels showing ontology properties
edge_labels = {
    (u, v): data.get("ontology_property").name if "ontology_property" in data else data.get("relationship", "")
    for u, v, data in G_hpt.edges(data=True)
}

# Add edge labels to show relationships
edge_labels = nx.get_edge_attributes(G_hpt, "relationship")
nx.draw_networkx_edge_labels(G_hpt, pos_hpt, edge_labels=edge_labels, font_size=8)

# Add legend
legend_elements_hpt = [
    plt.Line2D([0], [0], marker="o", color="w", label="Engine", markerfacecolor="#5D3FD3", markersize=10),  # Dark purple
    plt.Line2D([0], [0], marker="o", color="w", label="Cost", markerfacecolor="#FA8072", markersize=10),  # Salmon
    plt.Line2D([0], [0], marker="o", color="w", label="Fault", markerfacecolor="#FFD700", markersize=10),  # Yellow
    plt.Line2D([0], [0], marker="o", color="w", label="Part", markerfacecolor="#32CD32", markersize=10),  # Lime green
    plt.Line2D([0], [0], marker="o", color="w", label="Maintenance Action", markerfacecolor="#ADD8E6", markersize=10)  # Light blue
]

plt.legend(handles=legend_elements_hpt, loc="lower center", bbox_to_anchor=(0.5, -0.1), 
           title="Node Categories", ncol=3, frameon=False)

# Add title to the graph
plt.title("Knowledge Graph of HPT Parts, Faults, Maintenance Actions, and Costs", fontsize=16)

# Remove axes for better visualization
plt.axis("off")

# Show the graph
plt.show()
