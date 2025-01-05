import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------
# Step 1: Create the Knowledge Graph
# -------------------------------
G = nx.DiGraph()

# Nodes - Components with Attributes
G.add_nodes_from([
    ("Impeller", {"Type": "Centrifugal Compressor", "Failure Rate (%)": 2.5, "Inspection Interval (hrs)": 5000, "Cost ($)": 5000}),
    ("Diffuser", {"Type": "Centrifugal Compressor", "Failure Rate (%)": 1.8, "Inspection Interval (hrs)": 6000, "Cost ($)": 4000}),
    ("Scroll", {"Type": "Centrifugal Compressor", "Failure Rate (%)": 1.2, "Inspection Interval (hrs)": 7000, "Cost ($)": 3000}),
    ("Nozzle Blades", {"Type": "Axial-Flow Turbine", "Failure Rate (%)": 3.0, "Inspection Interval (hrs)": 4500, "Cost ($)": 7000}),
    ("Rotor Blades", {"Type": "Axial-Flow Turbine", "Failure Rate (%)": 4.2, "Inspection Interval (hrs)": 4000, "Cost ($)": 8000}),
    ("Exducer", {"Type": "Radial-Inflow Turbine", "Failure Rate (%)": 2.1, "Inspection Interval (hrs)": 5500, "Cost ($)": 3000}),
    ("Burning Zone", {"Type": "Combustor", "Failure Rate (%)": 2.8, "Inspection Interval (hrs)": 4500, "Cost ($)": 9000})
])

# Edges - Relationships with Failure Dependencies
G.add_edges_from([
    ("Impeller", "Diffuser", {"Relationship": "Transfers Kinetic Energy To", "Dependency": "Failure Causes Pressure Loss"}),
    ("Diffuser", "Scroll", {"Relationship": "Converts Velocity Into Pressure", "Dependency": "Failure Causes Flow Imbalance"}),
    ("Scroll", "Nozzle Blades", {"Relationship": "Outputs Compressed Fluid To", "Dependency": "Failure Causes Overheating"}),
    ("Nozzle Blades", "Rotor Blades", {"Relationship": "Accelerates and Directs Flow To", "Dependency": "Failure Reduces Efficiency"}),
    ("Rotor Blades", "Exducer", {"Relationship": "Guides Flow To", "Dependency": "Failure Increases Vibrations"}),
    ("Burning Zone", "Nozzle Blades", {"Relationship": "Delivers Heated Air To", "Dependency": "Failure Causes Temperature Drop"})
])

# -------------------------------
# Step 2: Visualize Graph - Dependencies
# -------------------------------
plt.figure(1, figsize=(14, 12))
pos = nx.circular_layout(G, scale=2)

# Draw Nodes
nx.draw(
    G, pos, with_labels=True, node_size=3000, node_color='lightblue',
    font_size=13, font_weight='bold', font_color='blue', arrowsize=45, connectionstyle='arc3,rad=0.2' 
)

# Draw Edges with Dependencies
edges = nx.get_edge_attributes(G, 'Dependency')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges, font_size=14, label_pos=0.3, font_color='red')

plt.title("Figure 1: Gas Turbine - Dependencies (Circular Layout)")
plt.show()

# -------------------------------
# Step 3: Visualize Graph - Relationships
# -------------------------------
plt.figure(2, figsize=(14, 12))
pos = nx.circular_layout(G)

# Draw Nodes
nx.draw(
    G, pos, with_labels=True, node_size=3500, node_color='lightgreen',
    font_size=14, font_weight='bold', font_color='blue', arrowsize=30, connectionstyle='arc3,rad=0.2' 
)

# Draw Edges with Relationships
edges = nx.get_edge_attributes(G, 'Relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges, font_size=14, label_pos=0.3, font_color='purple')

plt.title("Figure 2: Gas Turbine - Relationships (Circular Layout)")
plt.show()

# -------------------------------
# Step 4: Visualize Failure Rates vs Inspection Intervals
# -------------------------------
plt.figure(3, figsize=(10, 6))

# Extract Data for Plot
nodes = G.nodes(data=True)
components = [node for node, attr in nodes if attr['Type'] != 'Engine']
failure_rates = [attr['Failure Rate (%)'] for node, attr in nodes if attr['Type'] != 'Engine']
inspection_intervals = [attr['Inspection Interval (hrs)'] for node, attr in nodes if attr['Type'] != 'Engine']

plt.scatter(inspection_intervals, failure_rates, color='orange', s=200)

# Label Points
for i, comp in enumerate(components):
    plt.text(inspection_intervals[i], failure_rates[i], comp, fontsize=10, ha='right')

plt.title("Figure 3: Failure Rates vs Inspection Intervals")
plt.xlabel("Inspection Interval (hrs)")
plt.ylabel("Failure Rate (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------
# Step 5: Maintenance Costs Simulation
# -------------------------------

# Create DataFrame for Maintenance Costs
data = {
    "Component": ["Impeller", "Diffuser", "Scroll", "Nozzle Blades", "Rotor Blades", "Exducer", "Burning Zone"],
    "Failure Rate (%)": [2.5, 1.8, 1.2, 3.0, 4.2, 2.1, 2.8],
    "Inspection Interval (hrs)": [5000, 6000, 7000, 4500, 4000, 5500, 4500],
    "Cost ($)": [5000, 4000, 3000, 7000, 8000, 3000, 9000]
}
df = pd.DataFrame(data)

# Calculate 10-year costs
df["Projected Cost (10 years)"] = df["Cost ($)"] * (87600 / df["Inspection Interval (hrs)"])

# Plot Costs
plt.figure(4, figsize=(10, 6))
df.plot(x="Component", y="Projected Cost (10 years)", kind="bar", color="salmon", legend=False)
plt.title("Projected Maintenance Costs Over 10 Years")
plt.ylabel("Cost ($)")
plt.xlabel("Component")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Export to CSV (optional)
output_path = "/Users/dustin_caravaglia/Documents/kay_geez/university_ontology/gas_turbine_maintenance_costs.csv"
df.to_csv(output_path, index=False)
print(f"CSV saved successfully to: {output_path}")
