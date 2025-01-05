import random
import matplotlib.pyplot as plt
import networkx as nx
from owlready2 import *
import matplotlib.patches as mpatches
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

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
for eng in engines:
    G.add_node(eng, Type="Engine")

# Nodes - Components
components = [
    "Impeller", "Diffuser", "Scroll", "Nozzle Blades", "Rotor Blades",
    "Exducer", "Burning Zone", "Combustion Liner", "Transition Duct",
    "Compressor Rotor", "Compressor Stator", "Seal Plate"
]
for comp in components:
    G.add_node(comp, Type="Component", FailureRate=random.uniform(1.0, 5.0), Cost=random.randint(3000, 15000))

# Nodes - Faults with Costs
faults = {
    "Pressure Loss": {"Manual Number": "RM-001", "Reference": "Section 5.2 - Nozzle Blade Check"},
    "Overheating": {"Manual Number": "RM-002", "Reference": "Section 6.3 - Rotor Blade Cooling System"},
    "Seal Leakage": {"Manual Number": "RM-003", "Reference": "Section 4.1 - Combustion Liner Seals"},
    "Efficiency Loss": {"Manual Number": "RM-004", "Reference": "Section 7.2 - Diffuser Efficiency Test"},
    "Vibration Stress": {"Manual Number": "RM-005", "Reference": "Section 3.5 - Impeller Inspection"}
}
for fault, details in faults.items():
    G.add_node(fault, Type="Fault", ManualNumber=details["Manual Number"], Reference=details["Reference"])

# Nodes - Failure Modes
failure_modes = [
    "Corrosion Damage", "Thermal Stress", "Seal Leakage", 
    "Fatigue Cracking", "Overheating", "Vibration Stress",
    "Erosion Damage", "Foreign Object Damage (FOD)"
]
for mode in failure_modes:
    G.add_node(mode, Type="FailureMode")

# Add Relationships
G.add_edges_from([
    ("Engine_A", "Nozzle Blades"),
    ("Nozzle Blades", "Pressure Loss"),
    ("Rotor Blades", "Overheating"),
    ("Combustion Liner", "Seal Leakage"),
    ("Diffuser", "Efficiency Loss"),
    ("Impeller", "Vibration Stress")
])

# -------------------------------
# Step 3: Predictive Maintenance
# -------------------------------
def calculate_risk_scores():
    """Calculate normalized risk scores for components."""
    risk_scores = {}
    results = []

    # Temporary list to find max score
    raw_scores = []

    for node, data in G.nodes(data=True):
        if data["Type"] == "Component":
            # Retrieve attributes
            failure_rate = data.get("FailureRate", 1.0) / 100  # Normalize %
            cost = data.get("Cost", 5000)
            inspection_interval = random.randint(3000, 5000)  # Simulated intervals

            # Calculate raw risk score
            risk_score = (failure_rate * cost) / inspection_interval
            raw_scores.append(risk_score)  # Collect raw scores for normalization

    # Normalize scores to 0–100 scale
    max_risk_score = max(raw_scores) if raw_scores else 1  # Avoid division by zero

    for node, data in G.nodes(data=True):
        if data["Type"] == "Component":
            failure_rate = data.get("FailureRate", 1.0) / 100
            cost = data.get("Cost", 5000)
            inspection_interval = random.randint(3000, 5000)

            # Recalculate risk score and normalize
            risk_score = (failure_rate * cost) / inspection_interval
            normalized_score = 100 * (risk_score / max_risk_score)
            risk_scores[node] = round(normalized_score, 2)

            # Collect results for display
            results.append(f"{node}: {risk_scores[node]}% Risk Score")

    # Display results
    messagebox.showinfo("Predictive Risk Scores", "\n".join(results))

    return risk_scores


def procurement_alerts():
    """Generate proactive procurement alerts with lead times and availability checks."""
    alerts = []
    for node, data in G.nodes(data=True):
        if data["Type"] == "Component":
            failure_rate = data.get("FailureRate", 1.0)

            # Simulated data for proactive procurement
            lead_time = random.randint(4, 8)  # Weeks
            stock_level = random.randint(0, 5)  # Simulated stock availability
            reorder_threshold = 2  # Minimum stock threshold for alerts

            # Trigger procurement alerts for high-risk components
            if failure_rate > 3.0:  # Threshold for alerts
                if stock_level <= reorder_threshold:
                    alerts.append(f"{node}: High Risk—Lead Time: {lead_time} weeks. Check stock levels and reorder.")
                else:
                    alerts.append(f"{node}: Medium Risk—Lead Time: {lead_time} weeks. Monitor stock closely.")

    # Display procurement alerts
    if alerts:
        messagebox.showwarning("Proactive Procurement Alerts", "\n".join(alerts))
    else:
        messagebox.showinfo("Procurement Alerts", "All components are operating within safe limits.")


# -------------------------------
# Step 4: Graph Visualization
# -------------------------------
def draw_graph():
    """Displays the graph with nodes and edges."""
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)

    # Node Colors
    categories = nx.get_node_attributes(G, "Type")
    node_colors = [
        "#9370DB" if categories.get(node, "Unknown") == "Engine" else
        "#32CD32" if categories.get(node, "Unknown") == "Component" else
        "#FFD700" if categories.get(node, "Unknown") == "Fault" else
        "#FFA500" for node in G.nodes()
    ]

    # Draw Graph
    nx.draw(
        G, pos, with_labels=True, node_size=2000, node_color=node_colors,
        font_size=9, arrows=True, arrowsize=20
    )

    # Embed in GUI
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Gas Turbine Predictive Maintenance System")
root.geometry("1200x800")

frame_graph = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_controls = tk.Frame(root, bd=2, relief=tk.RAISED)
frame_controls.pack(side=tk.RIGHT, fill=tk.Y)

fault_dropdown = ttk.Combobox(frame_controls, values=list(faults.keys()), state="readonly")
fault_dropdown.set("Select a Fault")
fault_dropdown.pack(pady=10)

btn_draw_graph = ttk.Button(frame_controls, text="Show Graph", command=draw_graph)
btn_draw_graph.pack(pady=10)

btn_show_manual = ttk.Button(frame_controls, text="Show Manual", command=procurement_alerts)
btn_show_manual.pack(pady=10)

btn_calculate_risk = ttk.Button(frame_controls, text="Calculate Risk Scores", command=calculate_risk_scores)
btn_calculate_risk.pack(pady=10)

btn_procurement = ttk.Button(frame_controls, text="Procurement Alerts", command=procurement_alerts)
btn_procurement.pack(pady=10)

root.mainloop()
