import pandas as pd
import matplotlib.pyplot as plt

# Load Data
data = {
    "Component": [
        "High-Speed Shaft Bearing", "Intermediate Shaft Bearing", "Generator Drive-End Bearing",
        "Generator Non-Drive-End Bearing", "Ring Gear", "Planetary Gear", "Sun Gear",
        "Oil Pump", "Oil Filter", "Vibration Sensor", "Particle Counter"
    ],
    "Failure Rate (%)": [8.0, 7.5, 6.5, 6.0, 6.0, 5.5, 5.0, 4.5, 3.5, 2.0, 1.8],
    "Inspection Interval (hrs)": [3000, 3500, 4000, 4200, 5000, 4500, 4000, 3500, 3600, 2000, 2200],
    "Cost ($)": [15000, 14000, 12000, 11000, 12000, 14000, 13000, 9000, 8000, 5000, 4500],
    "Projected Cost (10 years)": [
        438000.0, 350400.0, 262800.0, 229428.57, 210240.0, 272533.33, 284700.0,
        225257.14, 194666.67, 219000.0, 179181.82
    ]
}

df = pd.DataFrame(data)

# Plot 1: Failure Rate Comparison
plt.figure(figsize=(10, 6))
plt.bar(df['Component'], df['Failure Rate (%)'], color='orange')
plt.title('Failure Rate Comparison')
plt.xlabel('Component')
plt.ylabel('Failure Rate (%)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 2: Projected Maintenance Costs Over 10 Years
plt.figure(figsize=(10, 6))
plt.bar(df['Component'], df['Projected Cost (10 years)'], color='salmon')
plt.title('Projected Maintenance Costs Over 10 Years')
plt.xlabel('Component')
plt.ylabel('Cost ($)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 3: Inspection Interval vs Cost
plt.figure(figsize=(10, 6))
plt.scatter(df['Inspection Interval (hrs)'], df['Cost ($)'], color='green')
for i in range(len(df)):
    plt.text(df['Inspection Interval (hrs)'][i], df['Cost ($)'][i], df['Component'][i], fontsize=8)
plt.title('Inspection Interval vs Cost')
plt.xlabel('Inspection Interval (hrs)')
plt.ylabel('Cost ($)')
plt.grid(True)
plt.tight_layout()
plt.show()
