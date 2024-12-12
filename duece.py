# Import necessary libraries
import matplotlib.pyplot as plt
import networkx as nx

# Initialize the knowledge graph
G_hpt = nx.DiGraph()

# Define categories
categories_hpt = [
    "Engine", "Part", "Fault", "Maintenance Action", "Cost", "Event"
]

# Define a limited set of engines
engines = [
    "Rolls-Royce BR700-715A1-30", 
    "General Electric CF34-8C5B1"
]

# Define a limited set of HPT parts
parts_hpt = [
    "HPT Stage 1 Disk", "HPT Blades (Stage 1)", "HPT Blades (Stage 2)"
]

# Define a limited set of faults
faults_hpt = [
    "Low Cycle Fatigue (LCF)", "Blade Tip Burnout", "Braze Failure"
]

# Define a limited set of maintenance actions
actions_hpt = [
    "Replace HPT Disk", "Inspect Seal Integrity", "Recoat Blade"
]

# Define a limited set of costs
costs_hpt = [
    "$10,000", "$15,000"
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
for engine, part in zip(engines, parts_hpt):
    G_hpt.add_edge(engine, part, relationship="contains component")

# Parts -> Faults
for part, fault in zip(parts_hpt, faults_hpt):
    G_hpt.add_edge(part, fault, relationship="has fault")

# Faults -> Maintenance Actions
for fault, action in zip(faults_hpt, actions_hpt):
    G_hpt.add_edge(fault, action, relationship="is addressed by")

# Faults -> Costs
for fault, cost in zip(faults_hpt, costs_hpt):
    G_hpt.add_edge(fault, cost, relationship="incurs cost")

# Visualize the graph
plt.figure(figsize=(10, 8))

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
nx.draw_networkx_nodes(G_hpt, pos_hpt, node_color=node_colors_hpt, node_size=1800, alpha=0.9)  # Increased node size
nx.draw_networkx_edges(G_hpt, pos_hpt, arrowstyle="->", arrowsize=15, edge_color="gray")  # Slightly larger arrow size
nx.draw_networkx_labels(G_hpt, pos_hpt, font_size=12, font_color="black", font_weight="bold")  # Increased font size for labels

# Add edge labels showing ontology properties
edge_labels = nx.get_edge_attributes(G_hpt, "relationship")
nx.draw_networkx_edge_labels(G_hpt, pos_hpt, edge_labels=edge_labels, font_size=10)  # Increased font size for edge labels

# Add legend
legend_elements_hpt = [
    plt.Line2D([0], [0], marker="o", color="w", label="Engine", markerfacecolor="#5D3FD3", markersize=12),  # Dark purple
    plt.Line2D([0], [0], marker="o", color="w", label="Cost", markerfacecolor="#FA8072", markersize=12),  # Salmon
    plt.Line2D([0], [0], marker="o", color="w", label="Fault", markerfacecolor="#FFD700", markersize=12),  # Yellow
    plt.Line2D([0], [0], marker="o", color="w", label="Part", markerfacecolor="#32CD32", markersize=12),  # Lime green
    plt.Line2D([0], [0], marker="o", color="w", label="Maintenance Action", markerfacecolor="#ADD8E6", markersize=12)  # Light blue
]

plt.legend(handles=legend_elements_hpt, loc="lower center", bbox_to_anchor=(0.5, -0.1), 
           title="Node Categories", ncol=3, frameon=False)

# Add title to the graph
plt.title("Maintenance Action Insights for High Pressure Turbine", fontsize=18)  # Slightly larger title font size

# Remove axes for better visualization
plt.axis("off")

# Show the graph
plt.show()
