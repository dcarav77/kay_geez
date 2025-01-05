import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Create the Knowledge Graph
G = nx.DiGraph()

# Nodes - Gearbox Components with Attributes
G.add_nodes_from([
    # Bearings
    ("High-Speed Shaft Bearing", {"Type": "Bearing", "Failure Rate (%)": 8.0, "Inspection Interval (hrs)": 3000, "Cost ($)": 15000}),
    ("Intermediate Shaft Bearing", {"Type": "Bearing", "Failure Rate (%)": 7.5, "Inspection Interval (hrs)": 3500, "Cost ($)": 14000}),
    ("Generator Drive-End Bearing", {"Type": "Bearing", "Failure Rate (%)": 6.5, "Inspection Interval (hrs)": 4000, "Cost ($)": 12000}),
    ("Generator Non-Drive-End Bearing", {"Type": "Bearing", "Failure Rate (%)": 6.0, "Inspection Interval (hrs)": 4200, "Cost ($)": 11000}),

    # Gears
    ("Ring Gear", {"Type": "Gear", "Failure Rate (%)": 6.0, "Inspection Interval (hrs)": 5000, "Cost ($)": 12000}),
    ("Planetary Gear", {"Type": "Gear", "Failure Rate (%)": 5.5, "Inspection Interval (hrs)": 4500, "Cost ($)": 14000}),
    ("Sun Gear", {"Type": "Gear", "Failure Rate (%)": 5.0, "Inspection Interval (hrs)": 4000, "Cost ($)": 13000}),

    # Lubrication System
    ("Oil Pump", {"Type": "Lubrication System", "Failure Rate (%)": 4.5, "Inspection Interval (hrs)": 3500, "Cost ($)": 9000}),
    ("Oil Filter", {"Type": "Lubrication System", "Failure Rate (%)": 3.5, "Inspection Interval (hrs)": 3600, "Cost ($)": 8000}),

    # Sensors
    ("Vibration Sensor", {"Type": "Sensor", "Failure Rate (%)": 2.0, "Inspection Interval (hrs)": 2000, "Cost ($)": 5000}),
    ("Particle Counter", {"Type": "Sensor", "Failure Rate (%)": 1.8, "Inspection Interval (hrs)": 2200, "Cost ($)": 4500})
])


# Edges - Relationships
G.add_edges_from([
    # Torque and Motion Transfer
    ("High-Speed Shaft Bearing", "Ring Gear", {"Relationship": "Supports and Transfers Load To"}),
    ("Ring Gear", "Planetary Gear", {"Relationship": "Transfers Torque To"}),
    ("Planetary Gear", "Sun Gear", {"Relationship": "Engages With"}),
    ("Sun Gear", "Generator Drive-End Bearing", {"Relationship": "Drives Motion To"}),

    # Lubrication and Monitoring
    ("Oil Pump", "High-Speed Shaft Bearing", {"Relationship": "Lubricates"}),
    ("Oil Filter", "Planetary Gear", {"Relationship": "Filters Oil For"}),
    ("Vibration Sensor", "Generator Drive-End Bearing", {"Relationship": "Monitors Vibration In"}),
    ("Particle Counter", "Oil Filter", {"Relationship": "Monitors Particle Buildup In"}),

    # Fault Dependencies
    ("Vibration Sensor", "High-Speed Shaft Bearing", {"Dependency": "Detects Wear In"}),
    ("Particle Counter", "Oil Filter", {"Dependency": "Detects Contamination In"})
])


# Step 2: Visualize the Graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightgreen', font_size=10, font_color='black')
edges = nx.get_edge_attributes(G, 'Relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
plt.title("Predictive Maintenance Ontology for Gearboxes")
plt.show()

# Step 3: Cost Simulation for Maintenance and Failures
# Create DataFrame
data = {
    "Component": ["Bearing", "Ring Gear", "Planetary Gear", "Shaft", "Housing", "Oil System"],
    "Failure Rate (%)": [8.0, 6.0, 5.5, 7.0, 3.0, 4.5],
    "Inspection Interval (hrs)": [3000, 5000, 4500, 4000, 6000, 3500],
    "Replacement Cost ($)": [15000, 12000, 14000, 11000, 8000, 9000]
}
df = pd.DataFrame(data)

# Calculate 10-year projected costs
inspection_hours = 87600  # 10 years in hours

df["Projected Cost (10 years)"] = df["Replacement Cost ($)"] * (inspection_hours / df["Inspection Interval (hrs)"])

# Plot Costs
plt.figure(figsize=(10, 6))
df.plot(x="Component", y="Projected Cost (10 years)", kind="bar", color="salmon", legend=False)
plt.title("Projected Maintenance Costs Over 10 Years for Gearbox Components")
plt.ylabel("Cost ($)")
plt.xlabel("Component")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Save CSV output
output_path = "gearbox_maintenance_costs.csv"
df.to_csv(output_path, index=False)
print("CSV saved successfully to:", output_path)

# Print DataFrame for debugging
print(df)
