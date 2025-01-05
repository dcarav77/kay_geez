import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Create the Knowledge Graph
G = nx.DiGraph()

# Nodes - Components with Attributes
G.add_nodes_from([
    ("High-Speed Shaft Bearing", {"Type": "Bearing", "Failure Rate (%)": 8.0, "Inspection Interval (hrs)": 3000, "Cost ($)": 15000}),
    ("Intermediate Shaft Bearing", {"Type": "Bearing", "Failure Rate (%)": 7.5, "Inspection Interval (hrs)": 3500, "Cost ($)": 14000}),
    ("Generator Drive-End Bearing", {"Type": "Bearing", "Failure Rate (%)": 6.5, "Inspection Interval (hrs)": 4000, "Cost ($)": 12000}),
    ("Generator Non-Drive-End Bearing", {"Type": "Bearing", "Failure Rate (%)": 6.0, "Inspection Interval (hrs)": 4200, "Cost ($)": 11000}),
    ("Ring Gear", {"Type": "Gear", "Failure Rate (%)": 6.0, "Inspection Interval (hrs)": 5000, "Cost ($)": 12000}),
    ("Planetary Gear", {"Type": "Gear", "Failure Rate (%)": 5.5, "Inspection Interval (hrs)": 4500, "Cost ($)": 14000}),
    ("Sun Gear", {"Type": "Gear", "Failure Rate (%)": 5.0, "Inspection Interval (hrs)": 4000, "Cost ($)": 13000}),
    ("Oil Pump", {"Type": "Lubrication System", "Failure Rate (%)": 4.5, "Inspection Interval (hrs)": 3500, "Cost ($)": 9000}),
    ("Oil Filter", {"Type": "Lubrication System", "Failure Rate (%)": 3.5, "Inspection Interval (hrs)": 3600, "Cost ($)": 8000}),
    ("Vibration Sensor", {"Type": "Sensor", "Failure Rate (%)": 2.0, "Inspection Interval (hrs)": 2000, "Cost ($)": 5000}),
    ("Particle Counter", {"Type": "Sensor", "Failure Rate (%)": 1.8, "Inspection Interval (hrs)": 2200, "Cost ($)": 4500})
])

# Edges - Relationships with Failure Dependencies
G.add_edges_from([
    ("High-Speed Shaft Bearing", "Ring Gear", {"Relationship": "Supports and Transfers Load To", "Dependency": "Bearing Failure Causes Gear Misalignment"}),
    ("Ring Gear", "Planetary Gear", {"Relationship": "Transfers Torque To", "Dependency": "Gear Failure Causes Torque Loss"}),
    ("Planetary Gear", "Sun Gear", {"Relationship": "Engages With", "Dependency": "Gear Damage Causes System Shutdown"}),
    ("Sun Gear", "Generator Drive-End Bearing", {"Relationship": "Drives Motion To", "Dependency": "Failure Causes Misalignment"}),
    ("Oil Pump", "High-Speed Shaft Bearing", {"Relationship": "Lubricates", "Dependency": "Oil Failure Leads to Bearing Wear"}),
    ("Oil Filter", "Planetary Gear", {"Relationship": "Filters Oil For", "Dependency": "Filter Blockage Causes Contamination"}),
    ("Vibration Sensor", "Generator Drive-End Bearing", {"Relationship": "Monitors Vibration In", "Dependency": "Sensor Failure Misses Early Warnings"}),
    ("Particle Counter", "Oil Filter", {"Relationship": "Monitors Particle Buildup In", "Dependency": "Sensor Failure Skips Oil Contamination Alerts"})
])

# Figure 1: Circular Layout with Dependencies
plt.figure(1, figsize=(14, 12))
pos = nx.circular_layout(G)  # Circular layout for symmetry
nx.draw(
    G, pos, with_labels=True, node_size=3500, node_color='lightblue',
    font_size=12, font_weight='bold', font_color='blue', arrowsize=20  
)

# Draw edge labels for Dependencies
edges = nx.get_edge_attributes(G, 'Dependency')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges, font_size=15, label_pos=0.3)
plt.title("Figure 1: Gearbox Predictive Maintenance - Dependencies (Circular Layout)")
plt.show()

# Figure 2: Circular Layout with Relationships
plt.figure(2, figsize=(14, 12))
pos = nx.circular_layout(G)  # Circular layout for symmetry
nx.draw(
    G, pos, with_labels=True, node_size=3500, node_color='lightgreen',
    font_size=12, font_weight='bold', font_color='blue', arrowsize=20  
)

# Draw edge labels for Relationships
edges = nx.get_edge_attributes(G, 'Relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges, font_size=15, label_pos=0.3)
plt.title("Figure 2: Gearbox Predictive Maintenance - Relationships (Circular Layout)")
plt.show()

# Exporting CSV for Maintenance Costs
data = {
    "Component": [
        "High-Speed Shaft Bearing", "Intermediate Shaft Bearing", "Generator Drive-End Bearing",
        "Generator Non-Drive-End Bearing", "Ring Gear", "Planetary Gear", "Sun Gear",
        "Oil Pump", "Oil Filter", "Vibration Sensor", "Particle Counter"
    ],
    "Failure Rate (%)": [8.0, 7.5, 6.5, 6.0, 6.0, 5.5, 5.0, 4.5, 3.5, 2.0, 1.8],
    "Inspection Interval (hrs)": [3000, 3500, 4000, 4200, 5000, 4500, 4000, 3500, 3600, 2000, 2200],
    "Cost ($)": [15000, 14000, 12000, 11000, 12000, 14000, 13000, 9000, 8000, 5000, 4500]
}
df = pd.DataFrame(data)

# Calculate 10-year costs
df["Projected Cost (10 years)"] = df["Cost ($)"] * (87600 / df["Inspection Interval (hrs)"])

# Export to CSV
df.to_csv("gearbox_maintenance_costs.csv", index=False)
print("CSV saved successfully!")
