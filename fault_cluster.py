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
    class incurs_cost(Fault >> Cost): pass  # Link faults directly to costs

    # Create individuals for engines
    engine_individuals = [Engine(name=engine.replace(" ", "_")) for engine in [
        "Rolls-Royce_BR700-715A1-30", 
        "Rolls-Royce_BR700-715B1-30", 
        "General_Electric_CF34-8C5B1"
    ]]

    # Create individuals for parts
    part_individuals = [Part(name=part.replace(" ", "_")) for part in [
        "HPT_Stage_1_Disk", "HPT_Stage_2_Disk", "HPT_Torque_Shaft", 
        "HPT_Interstage_Seal_Disk", "HPT_Blades_(Stage_1)", "HPT_Blades_(Stage_2)"
    ]]

    # Create individuals for faults
    fault_individuals = [Fault(name=fault.replace(" ", "_")) for fault in [
        "Braze_Failure", "Tip_Cap_Loss", "Creep_Deformation", 
        "Low_Cycle_Fatigue_(LCF)", "High_Cycle_Fatigue_(HCF)", 
        "Seal_Leakage", "Disk_Cracking", "Blade_Tip_Burnout"
    ]]

# Initialize the knowledge graph
G_hpt = nx.DiGraph()

# Add nodes and categorize them
for engine in engine_individuals:
    G_hpt.add_node(engine.name, category="Engine")

for part in part_individuals:
    G_hpt.add_node(part.name, category="Part")

for fault in fault_individuals:
    G_hpt.add_node(fault.name, category="Fault")

# Add regular edges for context
for i, part in enumerate(part_individuals):
    engine = engine_individuals[i % len(engine_individuals)].name
    fault = random.choice(fault_individuals).name
    G_hpt.add_edge(engine, part.name, relationship="contains_component")
    G_hpt.add_edge(part.name, fault, relationship="has_fault")

# Add a disproportionately large number of edges to HPT_Blades_(Stage_1)
highlight_part = "HPT_Blades_(Stage_1)"
highlight_engine = "Rolls-Royce_BR700-715A1-30"

# Add connection to its engine
G_hpt.add_edge(highlight_engine, highlight_part, relationship="contains_component")

# Create dozens of connections from HPT_Blades_(Stage_1) to faults
for _ in range(100):  # 100 edges for emphasis
    fault = random.choice(fault_individuals).name
    G_hpt.add_edge(highlight_part, fault, relationship="has_fault")

# Node colors
node_colors = [
    "#5D3FD3" if G_hpt.nodes[node]["category"] == "Engine" else  # Dark purple for Engine
    "#32CD32" if G_hpt.nodes[node]["category"] == "Part" else  # Lime green for Part
    "#FFD700" if G_hpt.nodes[node]["category"] == "Fault" else  # Yellow for Fault
    "gray"
    for node in G_hpt.nodes()
]

# Visualize the graph
plt.figure(figsize=(20, 15))
pos_hpt = nx.spring_layout(G_hpt, seed=42)  # Spring layout for better grouping

nx.draw_networkx_nodes(G_hpt, pos_hpt, node_color=node_colors, node_size=800, alpha=0.9)
nx.draw_networkx_edges(G_hpt, pos_hpt, width=1.0, alpha=0.7, edge_color="gray")
nx.draw_networkx_labels(G_hpt, pos_hpt, font_size=10, font_color="black", font_weight="bold")

# Add edge labels for relationships
edge_labels = nx.get_edge_attributes(G_hpt, "relationship")
nx.draw_networkx_edge_labels(G_hpt, pos_hpt, edge_labels=edge_labels, font_size=8)

# Add legend
legend_elements = [
    plt.Line2D([0], [0], marker="o", color="w", label="Engine", markerfacecolor="#5D3FD3", markersize=10),  # Dark purple
    plt.Line2D([0], [0], marker="o", color="w", label="Part", markerfacecolor="#32CD32", markersize=10),  # Lime green
    plt.Line2D([0], [0], marker="o", color="w", label="Fault", markerfacecolor="#FFD700", markersize=10)  # Yellow
]
plt.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)

plt.title("Fault Cluster: HPT Blades (Stage 1) & Rolls-Royce Engine", fontsize=16)
plt.axis("off")
plt.show()
