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
        "Rolls-Royce BR700-715A1-30", 
        "Rolls-Royce BR700-715B1-30", 
        "Rolls-Royce BR700-715C1-30", 
        "CL-600-2B19_Series", 
        "General_Electric_CF34-8C5B1",
        "Pratt_&_Whitney_PW1500G"
    ]]

    # Create individuals for parts
    part_individuals = [Part(name=part.replace(" ", "_")) for part in [
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
    ]]

    # Create individuals for faults
    fault_individuals = [Fault(name=fault.replace(" ", "_")) for fault in [
        "Braze Failure", "Tip Cap Loss", "Creep Deformation", 
        "Low Cycle Fatigue (LCF)", "High Cycle Fatigue (HCF)", 
        "Thermal Fatigue Cracking", "Stress Concentration Fracture", 
        "Blade/Disk Dovetail Cracking", "Vibratory Stress Failure", 
        "Overtemperature Induced Failure", "Seal Leakage", 
        "Disk Cracking", "Blade Tip Burnout", "Bolt Hole Fracture", 
        "Interstage Seal Erosion", "Tip Clearance Wear", 
        "Rotor Overspeed Damage", "Oxidation and Corrosion", 
        "Foreign Object Damage (FOD)", "HPT Blade Shear Failure"
    ]]

# Define cost ranges based on fault severity
fault_cost_map = {
    "Braze Failure": (10000, 15000),
    "Tip Cap Loss": (8000, 12000),
    "Creep Deformation": (15000, 20000),
    "Low Cycle Fatigue (LCF)": (20000, 30000),
    "High Cycle Fatigue (HCF)": (18000, 25000),
    "Thermal Fatigue Cracking": (15000, 25000),
    "Stress Concentration Fracture": (25000, 30000),
    "Blade/Disk Dovetail Cracking": (20000, 28000),
    "Vibratory Stress Failure": (12000, 18000),
    "Overtemperature Induced Failure": (20000, 30000),
    "Seal Leakage": (5000, 10000),
    "Disk Cracking": (15000, 25000),
    "Blade Tip Burnout": (8000, 12000),
    "Bolt Hole Fracture": (10000, 15000),
    "Interstage Seal Erosion": (5000, 10000),
    "Tip Clearance Wear": (5000, 10000),
    "Rotor Overspeed Damage": (25000, 30000),
    "Oxidation and Corrosion": (5000, 15000),
    "Foreign Object Damage (FOD)": (20000, 30000),
    "HPT Blade Shear Failure": (25000, 30000),
}

# Initialize the knowledge graph
G_hpt = nx.DiGraph()

# Add nodes and edges to the knowledge graph
for engine in engine_individuals:
    G_hpt.add_node(engine.name, category="Engine", ontology_class=engine)

for part in part_individuals:
    G_hpt.add_node(part.name, category="Part", ontology_class=part)

for fault in fault_individuals:
    G_hpt.add_node(fault.name, category="Fault", ontology_class=fault)
    
    fault_name = fault.name.replace("_", " ")
    if fault_name in fault_cost_map:
        # Assign cost as a numeric node
        min_cost, max_cost = fault_cost_map[fault_name]
        cost_value = random.randint(min_cost, max_cost)
        cost_node_name = f"${cost_value:,}"  # Format cost as "$XX,XXX"
        G_hpt.add_node(cost_node_name, category="Cost")
        G_hpt.add_edge(fault.name, cost_node_name, relationship="incurs_cost")

# Add part-to-fault and engine-to-part relationships
for i, part in enumerate(part_individuals):
    engine = engine_individuals[i % len(engine_individuals)].name
    fault = fault_individuals[i % len(fault_individuals)].name
    G_hpt.add_edge(engine, part.name, relationship="contains_component")
    G_hpt.add_edge(part.name, fault, relationship="has_fault")

# Visualize the graph
plt.figure(figsize=(18, 14))

# Define positions for nodes
pos_hpt = nx.spring_layout(G_hpt, seed=42)

# Node colors based on categories
categories_hpt = list(set(nx.get_node_attributes(G_hpt, "category").values()))
colors_hpt = plt.cm.tab20(range(len(categories_hpt)))

node_colors_hpt = [
    "#5D3FD3" if G_hpt.nodes[node]["category"] == "Engine" else  # Dark purple for Engine
    "#FA8072" if G_hpt.nodes[node]["category"] == "Cost" else  # Salmon for Cost nodes
    "#FFD700" if G_hpt.nodes[node]["category"] == "Fault" else  # Yellow for Fault
    "#32CD32" if G_hpt.nodes[node]["category"] == "Part" else  # Lime green for Part
    colors_hpt[categories_hpt.index(G_hpt.nodes[node]["category"])]
    for node in G_hpt.nodes()
]

# Draw nodes and edges
nx.draw_networkx_nodes(G_hpt, pos_hpt, node_color=node_colors_hpt, node_size=1200, alpha=0.9)
nx.draw_networkx_edges(G_hpt, pos_hpt, arrowstyle="->", arrowsize=10, edge_color="gray")
nx.draw_networkx_labels(G_hpt, pos_hpt, font_size=8, font_color="black", font_weight="bold")

# Add an arrow pointing to HPT Stage 1 Disk
highlight_node = "HPT_Stage_1_Disk"
highlight_pos = pos_hpt[highlight_node]
plt.annotate(
    "HPT Stage 1 Disk", xy=highlight_pos, xycoords="data",
    xytext=(highlight_pos[0] + 0.15, highlight_pos[1] + 0.15),  # Position the label further away
    arrowprops=dict(facecolor="red", arrowstyle="wedge,tail_width=0.7", linewidth=2),  # Larger arrow
    fontsize=14, fontweight="bold", color="red"  # Larger, bold, and red font
)

# Add edge labels showing relationships
edge_labels = nx.get_edge_attributes(G_hpt, "relationship")
nx.draw_networkx_edge_labels(G_hpt, pos_hpt, edge_labels=edge_labels, font_size=8)

# Add legend
legend_elements_hpt = [
    plt.Line2D([0], [0], marker="o", color="w", label="Engine", markerfacecolor="#5D3FD3", markersize=10),  # Dark purple
    plt.Line2D([0], [0], marker="o", color="w", label="Cost", markerfacecolor="#FA8072", markersize=10),  # Salmon
    plt.Line2D([0], [0], marker="o", color="w", label="Fault", markerfacecolor="#FFD700", markersize=10),  # Yellow
    plt.Line2D([0], [0], marker="o", color="w", label="Part", markerfacecolor="#32CD32", markersize=10)  # Lime green
]

plt.legend(handles=legend_elements_hpt, loc="lower center", bbox_to_anchor=(0.5, -0.1),
           title="Node Categories", ncol=3, frameon=False)

# Add title to the graph
plt.title(" Ship Maintenance Knowledge Graph", fontsize=16)

# Remove axes for better visualization
plt.axis("off")

# Show the graph
plt.show()

# Save the ontology
onto.save(file="hpt_ontology_with_costs.owl")
