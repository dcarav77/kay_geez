import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Faults and their cost ranges
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

# Generate random costs within ranges for each fault
data = []
for fault, (min_cost, max_cost) in fault_cost_map.items():
    cost = random.uniform(min_cost, max_cost)
    data.append({"Fault": fault, "Cost": cost})

# Create a DataFrame
df = pd.DataFrame(data)

# Sort the data by cost in descending order
df = df.sort_values(by="Cost", ascending=False)

# Plotting the faults and costs
plt.figure(figsize=(12, 8))
sns.barplot(x="Cost", y="Fault", data=df, palette="viridis")

# Add labels and title
plt.title("Faults and Their Costs", fontsize=16)
plt.xlabel("Cost ($)", fontsize=14)
plt.ylabel("Fault", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Show the plot
plt.show()
