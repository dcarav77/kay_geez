import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Create the Knowledge Graph
G = nx.DiGraph()

# Nodes - Components
G.add_nodes_from([
    ("Gearbox", {"Type": "Wind Turbine Component", "Failure Rate (%)": 25, "Replacement Cost ($)": 200000, "Inspection Interval (hrs)": 5000}),
    ("Bearings", {"Type": "Subcomponent", "Wear Rate (%)": 12, "Lubrication State": "Normal", "Temperature (°C)": 75}),
    ("Lubrication System", {"Type": "Subsystem", "Viscosity (cSt)": 46, "Contamination Level": "Low", "Replacement Interval (hrs)": 3000}),
    ("Gears", {"Type": "Mechanical Part", "Pitting Severity (%)": 10, "Contact Stress (MPa)": 200, "Surface Roughness (µm)": 0.4}),
    ("Sensors", {"Type": "Monitoring System", "Sensor Type": "Vibration/Temperature"})
])

# Edges - Relationships
G.add_edges_from([
    ("Gearbox", "Bearings", {"Relationship": "Contains"}),
    ("Gearbox", "Sensors", {"Relationship": "Monitored By"}),
    ("Bearings", "Gears", {"Relationship": "Connected To"}),
    ("Bearings", "Lubrication System", {"Relationship": "Lubricated By"}),
    ("Lubrication System", "Bearings", {"Relationship": "Prevents Wear In"}),
    ("Lubrication System", "Sensors", {"Relationship": "Monitored For"}),
    ("Sensors", "Bearings", {"Relationship": "Detects Vibration In"}),
    ("Sensors", "Lubrication System", {"Relationship": "Detects Temperature Anomalies In"})
])

# Step 2: Visualize the Graph
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_color='black')
edges = nx.get_edge_attributes(G, 'Relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
plt.title("Knowledge Graph for Wind Turbine Gearbox")
plt.show()

# Step 3: Maintenance Costs Simulation
data = {
    "Component": ["Gearbox", "Bearings", "Lubrication System", "Gears"],
    "Failure Rate (%)": [25, 12, 8, 15],
    "Inspection Interval (hrs)": [5000, 3000, 3000, 4000],
    "Replacement Cost ($)": [200000, 15000, 5000, 30000]
}
df = pd.DataFrame(data)

# Calculate 10-year costs
df["Projected Cost (10 years)"] = df["Replacement Cost ($)"] * (87600 / df["Inspection Interval (hrs)"])

# Plot Costs
plt.figure(figsize=(10, 6))
df.plot(x="Component", y="Projected Cost (10 years)", kind="bar", color="salmon", legend=False)
plt.title("Projected Maintenance Costs Over 10 Years")
plt.ylabel("Cost ($)")
plt.xlabel("Component")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

print(df)

# Export CSV
df.to_csv("gearbox_maintenance.csv", index=False)
