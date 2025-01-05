import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# -------------------------------
# Data and Graph Initialization
# -------------------------------

# Create Directed Graph
G = nx.DiGraph()

# Add Nodes - Components with Attributes
components = [
    ("High-Speed Shaft Bearing", {"Failure Rate (%)": 8.0, "Cost ($)": 15000, "Inspection Interval (hrs)": 3000}),
    ("Intermediate Shaft Bearing", {"Failure Rate (%)": 7.5, "Cost ($)": 14000, "Inspection Interval (hrs)": 3500}),
    ("Generator Drive-End Bearing", {"Failure Rate (%)": 6.5, "Cost ($)": 12000, "Inspection Interval (hrs)": 4000}),
    ("Ring Gear", {"Failure Rate (%)": 6.0, "Cost ($)": 12000, "Inspection Interval (hrs)": 5000}),
    ("Planetary Gear", {"Failure Rate (%)": 5.5, "Cost ($)": 14000, "Inspection Interval (hrs)": 4500}),
    ("Sun Gear", {"Failure Rate (%)": 5.0, "Cost ($)": 13000, "Inspection Interval (hrs)": 4000}),
    ("Oil Pump", {"Failure Rate (%)": 4.5, "Cost ($)": 9000, "Inspection Interval (hrs)": 3500}),
    ("Vibration Sensor", {"Failure Rate (%)": 2.0, "Cost ($)": 5000, "Inspection Interval (hrs)": 2000})
]
G.add_nodes_from(components)

# Add Edges - Dependencies
edges = [
    ("High-Speed Shaft Bearing", "Ring Gear"),
    ("Ring Gear", "Planetary Gear"),
    ("Planetary Gear", "Sun Gear"),
    ("Oil Pump", "High-Speed Shaft Bearing"),
    ("Vibration Sensor", "Generator Drive-End Bearing")
]
G.add_edges_from(edges)

# -------------------------------
# Functions
# -------------------------------

def draw_graph():
    """Displays the graph with nodes and edges."""
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.circular_layout(G)

    # Draw graph
    nx.draw(
        G, pos, with_labels=True, node_size=2000, node_color='lightblue',
        font_size=9, font_color='black', arrows=True, arrowsize=20
    )

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'Dependency')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='darkred')

    # Embed plot in GUI
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def calculate_health():
    """Calculates and displays the system health score."""
    total_weighted_score = 0
    max_score = 100  # Scale to 100
    total_components = len(components)

    for node, data in G.nodes(data=True):
        failure_rate = data["Failure Rate (%)"]
        cost = data["Cost ($)"]
        interval = data["Inspection Interval (hrs)"]

        # Weighted score: failure rate * cost / inspection interval
        score = failure_rate * cost / interval
        total_weighted_score += score

    # Normalize to a 100-point scale
    health_score = max_score - (total_weighted_score / total_components)
    health_label.config(text=f"System Health Score: {health_score:.2f}/100")

    # Generate recommendations
    recommendations = []
    for node, data in G.nodes(data=True):
        if data["Failure Rate (%)"] > 7.0:  # High-risk threshold
            recommendations.append(f"Inspect {node} (Failure Rate: {data['Failure Rate (%)']}%)")

    # Display recommendations
    if recommendations:
        messagebox.showwarning("Recommendations", "\n".join(recommendations))
    else:
        messagebox.showinfo("Recommendations", "All components are operating within acceptable limits.")

def export_csv():
    """Exports maintenance data to a CSV file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        data = []
        for node, attributes in G.nodes(data=True):
            attributes['Component'] = node
            data.append(attributes)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Success", f"Data exported successfully to {file_path}")

# -------------------------------
# GUI Setup
# -------------------------------

# Main Window
root = tk.Tk()
root.title("Wind Turbine Gearbox Monitoring")
root.geometry("1200x800")

# Frames
frame_graph = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_controls = tk.Frame(root, bd=2, relief=tk.RAISED)
frame_controls.pack(side=tk.RIGHT, fill=tk.Y)

# Buttons
btn_draw_graph = ttk.Button(frame_controls, text="Show Graph", command=draw_graph)
btn_draw_graph.pack(pady=10)

btn_calculate_health = ttk.Button(frame_controls, text="Calculate Health Score", command=calculate_health)
btn_calculate_health.pack(pady=10)

btn_export_csv = ttk.Button(frame_controls, text="Export to CSV", command=export_csv)
btn_export_csv.pack(pady=10)

# System Health Label
health_label = tk.Label(frame_controls, text="System Health Score: N/A", font=("Arial", 12))
health_label.pack(pady=20)

# -------------------------------
# Main Loop
# -------------------------------
root.mainloop()
