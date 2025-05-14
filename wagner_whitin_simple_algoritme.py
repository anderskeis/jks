import numpy as np
import dearpygui.dearpygui as dpg
from typing import List, Tuple, Optional, Any

# Optimal O(T^2) H-matrix calculation and return detailed plan
def wagner_whitin(
    demand: List[float], 
    setup_cost: List[float], 
    holding_cost: List[float]
) -> Tuple[float, List[int], List[str]]:
    """
    Solves the Wagner-Whitin lot-sizing problem using dynamic programming.

    Parameters
    ----------
    demand : list of float of length T
        demand d_t for periods t = 1..T.
    setup_cost : list of float of length T
        fixed ordering cost K_t for each period.
    holding_cost : list of float of length T
        per-unit holding cost h_t for carrying inventory from t to t+1.

    Returns
    -------
    min_total_cost : float
        Minimum total cost to satisfy all demands.
    schedule : list of int
        List of 1-indexed periods in which orders should be placed.
    detailed_plan_lines : list of str
        A list of strings, where each string describes an order in the plan.
    """
    T = len(demand)
    if T == 0:
        return 0.0, [], ["No demand data provided."]

    d = np.array(demand, dtype=float)
    K = np.array(setup_cost, dtype=float)
    h = np.array(holding_cost, dtype=float)

    # Precompute holding cost matrix H[j, t]
    H = np.zeros((T, T), dtype=float)
    for j_idx in range(T):
        current_sum_h_from_j = 0.0
        for t_idx in range(j_idx + 1, T):
            current_sum_h_from_j += h[t_idx-1]
            H[j_idx, t_idx] = H[j_idx, t_idx-1] + d[t_idx] * current_sum_h_from_j
            
    # DP arrays
    C = np.full(T + 1, np.inf)
    order_period = [-1] * (T + 1)
    
    C[0] = 0.0

    # Recurrence
    for t_dp in range(1, T + 1):
        for j_dp in range(1, t_dp + 1):
            current_total_cost = C[j_dp-1] + K[j_dp-1]
            if j_dp -1 < t_dp -1:
                current_total_cost += H[j_dp-1, t_dp-1]
            
            if current_total_cost < C[t_dp]:
                C[t_dp] = current_total_cost
                order_period[t_dp] = j_dp

    min_total_cost = C[T]

    # Backtrack to find schedule
    schedule = []
    t_backtrack = T
    while t_backtrack > 0:
        j_sched = order_period[t_backtrack]
        schedule.append(j_sched)
        t_backtrack = j_sched - 1
    schedule.reverse()

    # Generate detailed plan
    detailed_plan_lines = []
    if not schedule or min_total_cost == np.inf:
        if np.all(d == 0):
            detailed_plan_lines.append("No demand in any period. No orders needed.")
            min_total_cost = 0.0
        elif min_total_cost == np.inf:
            detailed_plan_lines.append("Could not find a valid production plan.")
        else:
            detailed_plan_lines.append("No orders are needed.")
    else:
        for i in range(len(schedule)):
            order_in_period_1_idx = schedule[i]
            order_period_0_idx = order_in_period_1_idx - 1

            if i + 1 < len(schedule):
                next_order_period_1_idx = schedule[i+1]
                end_coverage_period_0_idx = next_order_period_1_idx - 2
            else:
                end_coverage_period_0_idx = T - 1
            
            if order_period_0_idx <= end_coverage_period_0_idx:
                 quantity_to_order = np.sum(d[order_period_0_idx : end_coverage_period_0_idx + 1])
            else:
                 quantity_to_order = 0 

            line = (f"  Order in Period {order_in_period_1_idx}: "
                    f"Produce {quantity_to_order:.2f} units "
                    f"(to cover demand for periods {order_period_0_idx + 1} to {end_coverage_period_0_idx + 1})")
            detailed_plan_lines.append(line)
            
    return min_total_cost, schedule, detailed_plan_lines


# --- Dear PyGui specific code ---

def _help_text(message: str):
    """Adds a (?) mark with a tooltip in Dear PyGui."""
    dpg.add_text("(?)", color=[150, 150, 150])
    with dpg.tooltip(dpg.last_item()):
        dpg.add_text(message)

def parse_input_string(input_str: str) -> Optional[List[float]]:
    """Parses a comma-separated string of numbers into a list of floats."""
    if not input_str.strip():
        return []
    try:
        return [float(x.strip()) for x in input_str.split(',')]
    except ValueError:
        return None

_example_demand = [20, 0, 30, 10, 20, 30, 50, 23, 1435, 13, 13, 244, 11, 23, 12, 23, 12, 23, 12, 23, 12, 23, 12, 23, 33, 12, 1999, 34, 3243, 35, 12, 34, 76, 45, 344, 144, 122]
_example_setup_cost_single_val = 100.0
_example_holding_cost_single_val = 2.0

def use_example_data_callback(sender: Any, app_data: Any, user_data: Any):
    """Populates input fields with example data."""
    demand_str = ", ".join(map(str, _example_demand))
    dpg.set_value("demand_input", demand_str)
    dpg.set_value("setup_cost_input", str(_example_setup_cost_single_val))
    dpg.set_value("holding_cost_input", str(_example_holding_cost_single_val))
    dpg.set_value("status_text", "Example data loaded. Click 'Calculate'.")
    dpg.set_value("result_cost_text", "Minimum total cost: -")
    dpg.set_value("result_schedule_text", "Order schedule: -")
    dpg.set_value("result_plan_text", "")

def clear_input_callback(sender: Any, app_data: Any, user_data: Any):
    """Clears all input fields and resets result and status texts."""
    dpg.set_value("demand_input", "")
    dpg.set_value("setup_cost_input", "")
    dpg.set_value("holding_cost_input", "")
    dpg.set_value("status_text", "Inputs cleared.")
    dpg.set_value("result_cost_text", "Minimum total cost: -")
    dpg.set_value("result_schedule_text", "Order schedule: -")
    dpg.set_value("result_plan_text", "")

def calculate_callback(sender: Any, app_data: Any, user_data: Any):
    """Callback for the Calculate button."""
    dpg.set_value("status_text", "Calculating...")

    demand_str = dpg.get_value("demand_input")
    setup_cost_single_str = dpg.get_value("setup_cost_input")
    holding_cost_single_str = dpg.get_value("holding_cost_input")

    demand = parse_input_string(demand_str)
    
    setup_cost_single = None
    holding_cost_single = None
    
    error_messages = []
    if demand is None:
        error_messages.append("Invalid format for Demand. Use comma-separated numbers.")

    try:
        if not setup_cost_single_str.strip():
            error_messages.append("Setup Cost cannot be empty.")
        else:
            setup_cost_single = float(setup_cost_single_str.strip())
            if setup_cost_single < 0:
                error_messages.append("Setup cost cannot be negative.")
    except ValueError:
        error_messages.append("Invalid format for Setup Cost. Use a single number.")

    try:
        if not holding_cost_single_str.strip():
            error_messages.append("Holding Cost cannot be empty.")
        else:
            holding_cost_single = float(holding_cost_single_str.strip())
            if holding_cost_single < 0:
                error_messages.append("Holding cost cannot be negative.")
    except ValueError:
        error_messages.append("Invalid format for Holding Cost. Use a single number.")


    if error_messages:
        dpg.set_value("status_text", "Error: " + " | ".join(error_messages))
        return

    if demand is None:
        dpg.set_value("status_text", "Error: Critical input error.")
        return

    if not demand:
        error_messages.append("Demand data cannot be empty.")
    else:
        num_periods = len(demand)
        setup_cost = [setup_cost_single] * num_periods
        holding_cost = [holding_cost_single] * num_periods
        
        if any(d < 0 for d in demand):
             error_messages.append("Demand values cannot be negative.")

    if error_messages:
        dpg.set_value("status_text", "Error: " + " | ".join(error_messages))
        return
    
    if not demand:
        dpg.set_value("status_text", "No data to process.")
        dpg.set_value("result_cost_text", "Minimum total cost: -")
        dpg.set_value("result_schedule_text", "Order schedule: -")
        dpg.set_value("result_plan_text", "")
        return

    try:
        min_cost, schedule, detailed_plan = wagner_whitin(demand, setup_cost, holding_cost)

        dpg.set_value("result_cost_text", f"Minimum total cost: {min_cost:.2f}")
        if schedule:
            dpg.set_value("result_schedule_text", "Order schedule (1-indexed periods): " + ", ".join(map(str, schedule)))
        else:
            dpg.set_value("result_schedule_text", "Order schedule: No orders needed or plan not found.")
        
        dpg.set_value("result_plan_text", "\n".join(detailed_plan))
        dpg.set_value("status_text", "Calculation complete.")

    except Exception as e:
        dpg.set_value("status_text", f"An error occurred during calculation: {e}")
        dpg.set_value("result_cost_text", "Minimum total cost: -")
        dpg.set_value("result_schedule_text", "Order schedule: -")
        dpg.set_value("result_plan_text", "")


if __name__ == "__main__":
    dpg.create_context()

    # Define a dark theme
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll): # Apply to all items
            # Window and Frame Backgrounds
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 60, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 70, 70, 255))
            
            # Text
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) # White text
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (150, 150, 150, 255))
            
            # Buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 100, 200, 255)) # Blue buttons
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 120, 220, 255)) # Lighter blue on hover
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 140, 240, 255)) # Even lighter blue when active
            
            # Headers
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (70, 70, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (80, 80, 80, 255))

            # Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border, (70, 70, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))

            # Title Bar
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (40, 40, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (50, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (40, 40, 40, 255))

            # Scrollbar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (100, 100, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (120, 120, 120, 255))

            # Separator
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (70, 70, 70, 255))
            
            # Styling for a slightly more modern look (optional)
            # dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            # dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 3)

    dpg.bind_theme(global_theme) # Bind the theme globally

    with dpg.window(label="Wagner-Whitin Lot Sizing Calculator", tag="primary_window", width=800, height=700):
        with dpg.group(horizontal=True):
            dpg.add_text("Demand (comma-separated):")
            _help_text("Enter demand for each period, e.g., 20, 0, 30, 10")
        dpg.add_input_text(tag="demand_input", width=-1)

        with dpg.group(horizontal=True):
            dpg.add_text("Setup Cost (per period):")
            _help_text("Enter a single fixed setup cost, e.g., 100")
        dpg.add_input_text(tag="setup_cost_input", width=-1)

        with dpg.group(horizontal=True):
            dpg.add_text("Holding Cost (per unit, per period):")
            _help_text("Enter a single per-unit holding cost, e.g., 2")
        dpg.add_input_text(tag="holding_cost_input", width=-1)
        
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Calculate", callback=calculate_callback, width=120)
            dpg.add_button(label="Use Example Data", callback=use_example_data_callback, width=150)
            dpg.add_button(label="Clear Inputs", callback=clear_input_callback, width=120)
        
        dpg.add_spacer(height=10)
        dpg.add_text("", tag="status_text", color=[255, 0, 0])
        dpg.add_separator()
        dpg.add_spacer(height=10)

        dpg.add_text("--- Results ---", color=[200, 200, 200])
        dpg.add_text("Minimum total cost: -", tag="result_cost_text")
        dpg.add_text("Order schedule: -", tag="result_schedule_text")
        
        dpg.add_text("Detailed Order Plan:")
        dpg.add_input_text(tag="result_plan_text", multiline=True, readonly=True, width=-1, height=200)

    dpg.create_viewport(title='Wagner-Whitin Calculator', width=820, height=750)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
