# Import necessary libraries
import random
import matplotlib.pyplot as plt
import networkx as nx
from owlready2 import *

# Create and define the ontology
onto = get_ontology("http://example.org/ontology/hpt_ontology.owl")

with onto:
    # Define ontology classes
    class Engine(Thing): pass
    class Part(Thing): pass
    class Fault(Thing): pass
    class MaintenanceAction(Thing): pass
    class Cost(Thing): pass

    # Define object properties
    class contains_component(Engine >> Part): pass
    class has_fault(Part >> Fault): pass
    class is_addressed_by(Fault >> MaintenanceAction): pass
    class incurs_cost(MaintenanceAction >> Cost): pass

    # Create individuals for engines
    engine_individuals = [Engine(name=engine.replace(" ", "_")) for engine in [
        "Rolls-Royce BR700-715A1-30", 
        "Rolls-Royce BR700-715B1-30", 
        "Rolls-Royce BR700-715C1-30", 
        "CL-600-2B19 Series", 
        "General Electric CF34-8C5B1",
        "Pratt & Whitney PW1500G"
    ]]

    # Create individuals for parts
    part_individuals = [Part(name=part.replace(" ", "_")) for part in [
        "HPT Stage 1 Disk", "HPT Stage 2 Disk", "HPT Torque Shaft", 
        "HPT Interstage Seal Disk", "HPT Blades (Stage 1)", "HPT Blades (Stage 2)"
    ]]

    # Create individuals for faults
    fault_individuals = [Fault(name=fault.replace(" ", "_")) for fault in [
        "Braze Failure", "Tip Cap Loss", "Creep Deformation"
    ]]

    # Create individuals for maintenance actions
    action_individuals = [MaintenanceAction(name=action.replace(" ", "_")) for action in [
        "Replace HPT Disk", "Inspect Seal Integrity", "Recalibrate Torque Shaft"
    ]]

    # Create individuals for costs
    cost_individuals = [
        Cost(name=f"Cost_{i+1}", value=random.randint(8000, 30000))
        for i in range(len(part_individuals))
]

    # Map costs to parts
    for i, part in enumerate(part_individuals):
        part.has_cost = cost_individuals[i]

# Initialize the knowledge graph
G_hpt = nx.DiGraph()

# Add nodes to the knowledge graph using ontology individuals
for engine in engine_individuals:
    G_hpt.add_node(engine.name, category="Engine", ontology_class=engine)

for part in part_individuals:
    G_hpt.add_node(part.name, category="Part", ontology_class=part)

for fault in fault_individuals:
    G_hpt.add_node(fault.name, category="Fault", ontology_class=fault)

for action in action_individuals:
    G_hpt.add_node(action.name, category="Maintenance Action", ontology_class=action)

for cost in cost_individuals:
    G_hpt.add_node(cost.name, category="Cost", ontology_class=cost)

# Add edges to the knowledge graph
G_hpt.add_edge(engine_individuals[0].name, part_individuals[0].name, relationship="contains_component")
G_hpt.add_edge(part_individuals[0].name, fault_individuals[0].name, relationship="has_fault")
G_hpt.add_edge(fault_individuals[0].name, action_individuals[0].name, relationship="is_addressed_by")
G_hpt.add_edge(action_individuals[0].name, cost_individuals[0].name, relationship="incurs_cost")

# Add more edges to fully connect the graph
for i in range(1, len(part_individuals)):
    G_hpt.add_edge(engine_individuals[i % len(engine_individuals)].name, part_individuals[i].name, relationship="contains_component")
    G_hpt.add_edge(part_individuals[i].name, fault_individuals[i % len(fault_individuals)].name, relationship="has_fault")
    G_hpt.add_edge(fault_individuals[i % len(fault_individuals)].name, action_individuals[i % len(action_individuals)].name, relationship="is_addressed_by")
    G_hpt.add_edge(action_individuals[i % len(action_individuals)].name, cost_individuals[i % len(cost_individuals)].name, relationship="incurs_cost")

# Visualize the graph
plt.figure(figsize=(18, 14))

# Define positions for nodes
pos_hpt = nx.spring_layout(G_hpt, seed=42)

# Node colors based on categories
categories_hpt = list(set(nx.get_node_attributes(G_hpt, "category").values()))
colors_hpt = plt.cm.tab20(range(len(categories_hpt)))

# Set colors for specific node categories
node_colors_hpt = [
    "green" if G_hpt.nodes[node]["category"] == "Engine" else
    "#FA8072" if G_hpt.nodes[node]["category"] == "Cost" else  # Salmon color for Cost nodes
    "#FFD700" if G_hpt.nodes[node]["category"] == "Fault" else 
    "#32CD32" if G_hpt.nodes[node]["category"] == "Part" else
    colors_hpt[categories_hpt.index(G_hpt.nodes[node]["category"])]
    for node in G_hpt.nodes()
]

# Draw nodes and edges
nx.draw_networkx_nodes(G_hpt, pos_hpt, node_color=node_colors_hpt, node_size=1200, alpha=0.9)
nx.draw_networkx_edges(G_hpt, pos_hpt, arrowstyle="->", arrowsize=10, edge_color="gray")
nx.draw_networkx_labels(G_hpt, pos_hpt, font_size=8, font_color="black", font_weight="bold")

# Add edge labels showing relationships
edge_labels = nx.get_edge_attributes(G_hpt, "relationship")
nx.draw_networkx_edge_labels(G_hpt, pos_hpt, edge_labels=edge_labels, font_size=8)

# Add legend
legend_elements_hpt = [
    plt.Line2D([0], [0], marker="o", color="w", label=category, markersize=10, 
               markerfacecolor=("green" if category == "Engine" else
                                "#FA8072" if category == "Cost" else  # Salmon for Cost
                                "#FFD700" if category == "Fault" else
                                "#32CD32" if category == "Part" else
                                colors_hpt[i]))
    for i, category in enumerate(categories_hpt)
]

plt.legend(handles=legend_elements_hpt, loc="lower center", bbox_to_anchor=(0.5, -0.1), 
           title="Node Categories", ncol=3, frameon=False)

# Add title to the graph
plt.title("Knowledge Graph with Ontology of HPT Components, Faults, and Costs", fontsize=16)

# Remove axes for better visualization
plt.axis("off")

# Show the graph
plt.show()

# Save the ontology
onto.save(file="hpt_ontology.owl")
