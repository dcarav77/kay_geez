import random
import matplotlib.pyplot as plt
import networkx as nx
from owlready2 import *

# Create and define the ontology
onto = get_ontology("http://example.org/ontology/wind_turbine_ontology.owl")

with onto:
    # Define ontology classes
    class Gearbox(Thing): pass
    class Component(Thing): pass
    class Fault(Thing): pass
    class MaintenanceAction(Thing): pass
    class Cost(Thing): pass

    # Define object properties
    class contains_component(Gearbox >> Component): pass
    class has_fault(Component >> Fault): pass
    class is_addressed_by(Fault >> MaintenanceAction): pass
    class incurs_cost(Fault >> Cost): pass  # Link faults directly to costs

    # Create individuals for gearboxes
    gearbox_individuals = [Gearbox(name=gearbox.replace(" ", "_")) for gearbox in [
        "Gearbox_A1", "Gearbox_B2", "Gearbox_C3"
    ]]

    # Create individuals for components
    component_individuals = [Component(name=component.replace(" ", "_")) for component in [
        "High-Speed Shaft Bearing", "Intermediate Shaft Bearing", "Planetary Gear", 
        "Sun Gear", "Ring Gear", "Oil Pump", "Oil Filter", "Vibration Sensor", "Particle Counter"
    ]]

    # Create individuals for faults
    fault_individuals = [Fault(name=fault.replace(" ", "_")) for fault in [
        "Bearing Wear", "Gear Misalignment", "Oil Contamination", "Lubrication Failure",
        "Vibration Sensor Failure", "Particle Build-Up", "Seal Leakage", "Crack Formation"
    ]]

# Define cost ranges based on fault severity
fault_cost_map = {
    "Bearing Wear": (8000, 15000),
    "Gear Misalignment": (10000, 18000),
    "Oil Contamination": (5000, 12000),
    "Lubrication Failure": (9000, 14000),
    "Vibration Sensor Failure": (4000, 8000),
    "Particle Build-Up": (3000, 7000),
    "Seal Leakage": (6000, 11000),
    "Crack Formation": (15000, 25000)
}

# Initialize the knowledge graph
G_wtg = nx.DiGraph()

# Add nodes and edges to the knowledge graph
for gearbox in gearbox_individuals:
    G_wtg.add_node(gearbox.name, category="Gearbox")

for component in component_individuals:
    G_wtg.add_node(component.name, category="Component")

for fault in fault_individuals:
    G_wtg.add_node(fault.name, category="Fault")
    fault_name = fault.name.replace("_", " ")
    if fault_name in fault_cost_map:
        # Assign cost as a numeric node
        min_cost, max_cost = fault_cost_map[fault_name]
        cost_value = random.randint(min_cost, max_cost)
        cost_node_name = f"${cost_value:,}"
        G_wtg.add_node(cost_node_name, category="Cost")
        G_wtg.add_edge(fault.name, cost_node_name, relationship="incurs_cost")

# Add gearbox-to-component and component-to-fault relationships
for i, component in enumerate(component_individuals):
    gearbox = gearbox_individuals[i % len(gearbox_individuals)].name
    fault = fault_individuals[i % len(fault_individuals)].name
    G_wtg.add_edge(gearbox, component.name, relationship="contains_component")
    G_wtg.add_edge(component.name, fault, relationship="has_fault")

# Visualize the graph
plt.figure(figsize=(18, 14))

# Define positions for nodes
pos_wtg = nx.spring_layout(G_wtg, seed=42)

# Node colors based on categories
categories_wtg = list(set(nx.get_node_attributes(G_wtg, "category").values()))
colors_wtg = plt.cm.tab20(range(len(categories_wtg)))

node_colors_wtg = [
    "#5D3FD3" if G_wtg.nodes[node]["category"] == "Gearbox" else
    "#FA8072" if G_wtg.nodes[node]["category"] == "Cost" else
    "#FFD700" if G_wtg.nodes[node]["category"] == "Fault" else
    "#32CD32" for node in G_wtg.nodes()
]

# Draw nodes and edges
nx.draw_networkx_nodes(G_wtg, pos_wtg, node_color=node_colors_wtg, node_size=1500, alpha=0.9)
nx.draw_networkx_edges(G_wtg, pos_wtg, arrowstyle="->", arrowsize=15, edge_color="gray")
nx.draw_networkx_labels(G_wtg, pos_wtg, font_size=10, font_color="black", font_weight="bold")

# Add edge labels
edge_labels = nx.get_edge_attributes(G_wtg, "relationship")
nx.draw_networkx_edge_labels(G_wtg, pos_wtg, edge_labels=edge_labels, font_size=11, font_color='blue')

# Legend
legend_elements_wtg = [
    plt.Line2D([0], [0], marker="o", color="w", label="Gearbox", markerfacecolor="#5D3FD3", markersize=10),
    plt.Line2D([0], [0], marker="o", color="w", label="Cost", markerfacecolor="#FA8072", markersize=10),
    plt.Line2D([0], [0], marker="o", color="w", label="Fault", markerfacecolor="#FFD700", markersize=10),
    plt.Line2D([0], [0], marker="o", color="w", label="Component", markerfacecolor="#32CD32", markersize=10)
]

plt.legend(handles=legend_elements_wtg, loc="lower center", bbox_to_anchor=(0.5, -0.1),
           title="Node Categories", ncol=3, frameon=False)

plt.title("Wind Turbine Gearbox Maintenance Knowledge Graph", fontsize=16)
plt.axis("off")
plt.show()

# Save the ontology
onto.save(file="wind_turbine_ontology.owl")
