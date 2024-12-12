# Import necessary libraries
import random
import pandas as pd
import networkx as nx
from owlready2 import *
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Create and define the ontology
onto = get_ontology("http://example.org/ontology/hpt_ontology.owl")

with onto:
    # Define ontology classes
    class Engine(Thing): pass
    class Part(Thing): pass
    class Fault(Thing): pass
    class MaintenanceAction(Thing): pass
    class Cost(Thing): pass

    # Define object properties
    class contains_component(Engine >> Part): pass
    class has_fault(Part >> Fault): pass
    class is_addressed_by(Fault >> MaintenanceAction): pass
    class incurs_cost(Fault >> Cost): pass  # Link faults directly to costs

    # Create individuals for engines
    engine_individuals = [Engine(name=engine.replace(" ", "_")) for engine in [
        "Rolls-Royce BR700-715A1-30", 
        "Rolls-Royce BR700-715B1-30", 
        "Rolls-Royce BR700-715C1-30", 
        "CL-600-2B19_Series", 
        "General_Electric_CF34-8C5B1",
        "Pratt_&_Whitney_PW1500G"
    ]]

    # Create individuals for parts
    part_individuals = [Part(name=part.replace(" ", "_")) for part in [
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
    ]]

    # Create individuals for faults
    fault_individuals = [Fault(name=fault.replace(" ", "_")) for fault in [
        "Braze Failure", "Tip Cap Loss", "Creep Deformation", 
        "Low Cycle Fatigue (LCF)", "High Cycle Fatigue (HCF)", 
        "Thermal Fatigue Cracking", "Stress Concentration Fracture", 
        "Blade/Disk Dovetail Cracking", "Vibratory Stress Failure", 
        "Overtemperature Induced Failure", "Seal Leakage", 
        "Disk Cracking", "Blade Tip Burnout", "Bolt Hole Fracture", 
        "Interstage Seal Erosion", "Tip Clearance Wear", 
        "Rotor Overspeed Damage", "Oxidation and Corrosion", 
        "Foreign Object Damage (FOD)", "HPT Blade Shear Failure"
    ]]

    # Define cost ranges based on fault severity
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

# Initialize the knowledge graph
G_hpt = nx.DiGraph()

# Add nodes and edges to the knowledge graph
fault_data = []
for fault in fault_individuals:
    G_hpt.add_node(fault.name, category="Fault")
    fault_name = fault.name.replace("_", " ")
    if fault_name in fault_cost_map:
        min_cost, max_cost = fault_cost_map[fault_name]
        cost_value = random.randint(min_cost, max_cost)
        cost_node_name = f"${cost_value:,}"  # Format cost as "$XX,XXX"
        G_hpt.add_node(cost_node_name, category="Cost")
        G_hpt.add_edge(fault.name, cost_node_name, relationship="incurs_cost")
        fault_data.append({"Fault": fault_name, "Cost": cost_value})

# Assign operational status and calculate Fleet Readiness
for engine in engine_individuals:
    engine.operational_status = "Operational"  # Default status

non_operational_count = 0
for engine in engine_individuals:
    for part in part_individuals:
        if G_hpt.has_edge(engine.name, part.name):  # Check if the part belongs to the engine
            for fault in fault_individuals:
                if G_hpt.has_edge(part.name, fault.name):  # Check if the part has a fault
                    engine.operational_status = "Non-Operational"
                    non_operational_count += 1
                    break

total_aircraft = len(engine_individuals)
operational_count = total_aircraft - non_operational_count
fleet_readiness_level = (operational_count / total_aircraft) * 100

# Add Fleet Readiness DataFrame
readiness_data = {"Total Aircraft": total_aircraft, "Operational": operational_count, "Non-Operational": non_operational_count}
readiness_df = pd.DataFrame([readiness_data])

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("MRO Insights Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="kpi-dropdown",
        options=[
            {"label": "Fault Costs", "value": "Fault Costs"},
            {"label": "Fleet Readiness", "value": "Fleet Readiness"},
        ],
        value="Fault Costs",
        placeholder="Select KPI",
    ),
    dcc.Graph(id="kpi-graph"),
    html.Div(id="summary", style={"marginTop": 20}),
])

# Callback to update graph and summary
@app.callback(
    [Output("kpi-graph", "figure"), Output("summary", "children")],
    [Input("kpi-dropdown", "value")]
)
def update_graph(selected_kpi):
    if selected_kpi == "Fault Costs":
        fig = px.bar(
            pd.DataFrame(fault_data),
            x="Fault",
            y="Cost",
            title="Cost Associated with Each Fault",
            labels={"Fault": "Fault", "Cost": "Cost ($)"},
            color="Fault",
        )
        total_cost = sum(row["Cost"] for row in fault_data)
        summary = f"Total Cost of Faults: ${total_cost:,}"
    elif selected_kpi == "Fleet Readiness":
        fig = px.bar(
            readiness_df.melt(var_name="Status", value_name="Count"),
            x="Status",
            y="Count",
            title="Fleet Readiness Levels",
            labels={"Status": "Fleet Status", "Count": "Number of Aircraft"},
            color="Status",
        )
        summary = f"Fleet Readiness Level: {fleet_readiness_level:.2f}%"
    else:
        fig = px.bar()
        summary = "Select a KPI to visualize."
    return fig, summary

if __name__ == "__main__":
    app.run_server(debug=True)
