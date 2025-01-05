import random
import matplotlib.pyplot as plt
import networkx as nx
from owlready2 import *

# -------------------------------
# Step 1: Define Ontology
# -------------------------------
onto = get_ontology("http://example.org/ontology/gas_turbine_ontology.owl")

with onto:
    # Define ontology classes
    class Engine(Thing): pass
    class Component(Thing): pass
    class Fault(Thing): pass
    class FailureMode(Thing): pass
    class MaintenanceAction(Thing): pass

    # Define relationships
    class contains_component(Engine >> Component): pass
    class has_fault(Component >> Fault): pass
    class caused_by(Fault >> FailureMode): pass
    class is_addressed_by(Fault >> MaintenanceAction): pass

# -------------------------------
# Step 2: Create Knowledge Graph
# -------------------------------
G = nx.DiGraph()

# Nodes - Engines
engines = ["Engine_A", "Engine_B", "Engine_C"]
engine_nodes = [Engine(name=eng) for eng in engines]
for eng in engines:
    G.add_node(eng, Type="Engine")

# Nodes - Components
components = [
    "Impeller", "Diffuser", "Scroll", "Nozzle Blades", "Rotor Blades",
    "Exducer", "Burning Zone", "Combustion Liner", "Transition Duct",
    "Compressor Rotor", "Compressor Stator", "Seal Plate"
]
component_nodes = [Component(name=comp.replace(" ", "_")) for comp in components]
for comp in components:
    G.add_node(comp, Type="Component", FailureRate=random.uniform(1.0, 5.0), Cost=random.randint(3000, 15000))

# Nodes - Faults with Costs
faults = [
    "Pressure Loss", "Flow Imbalance", "Overheating", "Efficiency Loss",
    "Seal Leakage", "Blade Tip Burnout", "Bolt Hole Fracture",
    "Rotor Overspeed Damage", "Foreign Object Damage (FOD)"
]
fault_cost_map = {
    "Pressure Loss": (10000, 15000),
    "Flow Imbalance": (8000, 12000),
    "Overheating": (15000, 20000),
    "Efficiency Loss": (20000, 30000),
    "Seal Leakage": (5000, 10000),
    "Blade Tip Burnout": (8000, 12000),
    "Bolt Hole Fracture": (10000, 15000),
    "Rotor Overspeed Damage": (25000, 30000),
    "Foreign Object Damage (FOD)": (20000, 30000)
}
fault_nodes = [Fault(name=fault.replace(" ", "_")) for fault in faults]
for fault in faults:
    cost_value = random.randint(*fault_cost_map[fault])
    G.add_node(fault, Type="Fault", Cost=f"${cost_value}")

# Nodes - Failure Modes
failure_modes = [
    "Corrosion Damage", "Thermal Stress", "Seal Leakage", 
    "Fatigue Cracking", "Overheating", "Vibration Stress",
    "Erosion Damage", "Foreign Object Damage (FOD)"
]
failure_mode_nodes = [FailureMode(name=mode.replace(" ", "_")) for mode in failure_modes]
for mode in failure_modes:
    G.add_node(mode, Type="FailureMode")

# -------------------------------
# Step 3: Add Relationships
# -------------------------------
# Engine to Component Relationships
for i, comp in enumerate(components):
    engine = engines[i % len(engines)]
    G.add_edge(engine, comp, Relationship="contains_component")

# Component to Fault Relationships
for i, fault in enumerate(faults):
    comp = components[i % len(components)]
    G.add_edge(comp, fault, Relationship="has_fault")

# Fault to Failure Mode Relationships
for i, fault in enumerate(faults):
    failure_mode = failure_modes[i % len(failure_modes)]
    G.add_edge(fault, failure_mode, Relationship="caused_by")

# -------------------------------
# Step 4: Visualize Graph
# -------------------------------
plt.figure(figsize=(22, 22))

# Define node positions
pos = nx.spring_layout(G, seed=42, k=0.1)

# Draw Nodes
categories = nx.get_node_attributes(G, "Type")

node_colors = [
    "#9370DB" if categories.get(node, "Unknown") == "Engine" else  # Purple
    "#32CD32" if categories.get(node, "Unknown") == "Component" else  # Green
    "#FFD700" if categories.get(node, "Unknown") == "Fault" else  # Yellow
    "#FFA500" if categories.get(node, "Unknown") == "FailureMode" else  # Orange
    "#D3D3D3" for node in G.nodes()  # Default Grey
]

nx.draw(
    G, pos, node_color=node_colors, with_labels=True, node_size=1200,
    font_size=9, font_weight="bold"
)
nx.draw_networkx_edges(G, pos, arrowsize=12)

# Edge Labels
edges = nx.get_edge_attributes(G, "Relationship")
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edges, font_size=8, font_color="blue", font_weight="bold"
)

# -------------------------------
# Legend for Node Types
# -------------------------------
legend_elements = [
    plt.Line2D([0], [0], marker="o", color="w", label="Engine", markerfacecolor="#9370DB", markersize=10),
    plt.Line2D([0], [0], marker="o", color="w", label="Component", markerfacecolor="#32CD32", markersize=10),
    plt.Line2D([0], [0], marker="o", color="w", label="Fault", markerfacecolor="#FFD700", markersize=10),
    plt.Line2D([0], [0], marker="o", color="w", label="Failure Mode", markerfacecolor="#FFA500", markersize=10)
]

plt.legend(
    handles=legend_elements,
    loc="upper right",
    title="Node Categories",
    frameon=True  # Add a border around the legend
)
plt.subplots_adjust(bottom=0.2)  # Increase space for the legend
plt.tight_layout()  # Auto-fix layout spacing
plt.show()

# -------------------------------
# Step 5: Save Ontology
# -------------------------------
onto.save(file="gas_turbine_ontology_with_failure_modes.owl")
print("Ontology saved successfully!")
