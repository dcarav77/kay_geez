import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Define the parts, faults, costs, severities, and downtimes
parts = [
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
]

faults = [
    "Braze Failure", "Tip Cap Loss", "Creep Deformation", 
    "Low Cycle Fatigue (LCF)", "High Cycle Fatigue (HCF)", 
    "Thermal Fatigue Cracking", "Stress Concentration Fracture", 
    "Blade/Disk Dovetail Cracking", "Vibratory Stress Failure", 
    "Overtemperature Induced Failure", "Seal Leakage", 
    "Disk Cracking", "Blade Tip Burnout", "Bolt Hole Fracture", 
    "Interstage Seal Erosion", "Tip Clearance Wear", 
    "Rotor Overspeed Damage", "Oxidation and Corrosion", 
    "Foreign Object Damage (FOD)", "HPT Blade Shear Failure"
]

# Map costs and severities based on faults
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

# Randomly assign faults, costs, severities, and downtimes to parts
data = []
for part in parts:
    fault = random.choice(faults)
    cost_range = fault_cost_map[fault]
    cost = random.uniform(cost_range[0], cost_range[1])
    severity = random.randint(1, 5)
    downtime = random.randint(1, 10)
    data.append({"Part": part, "Fault": fault, "Cost": cost, "Severity": severity, "Downtime": downtime})

# Hard-code values for HPT Stage 1 Disk
data[0] = {
    "Part": "HPT Stage 1 Disk",
    "Fault": "Braze Failure",
    "Cost": 30000,  # High cost
    "Severity": 5,  # High severity
    "Downtime": 1   # Low downtime for max impact
}

# Create a DataFrame
df = pd.DataFrame(data)

# Calculate Impact Score
df["Impact Score"] = df["Cost"] * df["Severity"] / df["Downtime"]

# Sort by Impact Score in descending order
df = df.sort_values(by="Impact Score", ascending=False)

# Highlight "HPT Stage 1 Disk" by adjusting its label properties
highlight_part = "HPT Stage 1 Disk"

# Bar Plot for Impact Score by Part
plt.figure(figsize=(10, 20))
bar_plot = sns.barplot(
    x="Impact Score", y="Part", data=df, palette="coolwarm", dodge=False
)

# Highlight the text for "HPT Stage 1 Disk"
for text in bar_plot.get_yticklabels():
    if text.get_text() == highlight_part:
        text.set_fontweight("bold")  # Make it bold
        text.set_color("red")  # Change its color
        text.set_fontsize(12)  # Increase font size

# Add the Impact Score formula to the plot
plt.text(
    0.5, 1.05,
    "Impact Score = Cost × Severity / Downtime",
    horizontalalignment='center',
    verticalalignment='center',
    transform=plt.gca().transAxes,
    fontsize=10,
    color="black",
    bbox=dict(facecolor="white", alpha=0.5, edgecolor="black")
)

plt.title("Impact Score by Part")
plt.xlabel("Impact Score")
plt.ylabel("Part")
plt.show()

# Heatmap of Cost by Part and Downtime
plt.figure(figsize=(12, 10))
heatmap_data = df.pivot_table(values="Cost", index="Part", columns="Downtime")
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    cbar_kws={"label": "Cost ($)"},
)
plt.title("Cost by Part and Downtime")
plt.xlabel("Downtime (Days)")
plt.ylabel("Part")
plt.show()
