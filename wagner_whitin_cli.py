import numpy as np
import argparse
from typing import List, Tuple

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
            if j_dp - 1 < t_dp - 1:
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
            order_period_0_idx = order_in_period_1_idx - 1 # This is 'j' for K[j] and H[j, t]

            if i + 1 < len(schedule):
                next_order_period_1_idx = schedule[i+1]
                # This order covers demand up to the period *before* the next order.
                # 0-indexed: (next_order_period_1_idx - 1 - 1) = next_order_period_1_idx - 2.
                end_coverage_period_0_idx = next_order_period_1_idx - 2 
            else:
                # Last order, covers demand up to the end of the horizon T.
                # 0-indexed: T - 1.
                end_coverage_period_0_idx = T - 1
            
            # Calculate quantity for this specific order.
            # For a valid schedule, order_period_0_idx should be <= end_coverage_period_0_idx.
            if order_period_0_idx <= end_coverage_period_0_idx:
                 quantity_to_order = np.sum(d[order_period_0_idx : end_coverage_period_0_idx + 1])
            else:
                 # This case should ideally not be reached with a valid Wagner-Whitin schedule.
                 quantity_to_order = 0.0

            # Calculate cost for this specific order
            current_order_setup_cost = K[order_period_0_idx]
            current_order_holding_cost = 0.0
            
            # Holding cost is incurred if the order covers demand beyond the current period
            # and there's actual quantity being held.
            # H[j, t_end] = holding costs for demands d[j+1]...d[t_end] if produced at j.
            if quantity_to_order > 0 and order_period_0_idx < end_coverage_period_0_idx:
                current_order_holding_cost = H[order_period_0_idx, end_coverage_period_0_idx]
            
            current_order_total_cost = current_order_setup_cost + current_order_holding_cost

            line = (f"  Order in Period {order_in_period_1_idx}: "
                    f"Produce {quantity_to_order:.2f} units (Cost: {current_order_total_cost:.2f}) "
                    f"to cover demand for periods {order_period_0_idx + 1} to {end_coverage_period_0_idx + 1}.")
            detailed_plan_lines.append(line)
            
    return min_total_cost, schedule, detailed_plan_lines


def parse_comma_separated_list(value):
    """Parse a comma-separated string into a list of floats."""
    try:
        return [float(item.strip()) for item in value.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid format. Use comma-separated numbers (e.g., '10,20,30').")


def main():
    """Command-line interface for the Wagner-Whitin algorithm."""
    parser = argparse.ArgumentParser(description="Wagner-Whitin Lot Sizing Calculator CLI")
    parser.add_argument(
        "-d", "--demand", 
        type=parse_comma_separated_list,
        required=True,
        help="Comma-separated list of demands for each period (e.g., '10,20,30')"
    )
    parser.add_argument(
        "-s", "--setup-cost", 
        type=float, 
        required=True,
        help="Single fixed setup cost per period"
    )
    parser.add_argument(
        "-c", "--holding-cost", 
        type=float, 
        required=True,
        help="Single per-unit holding cost per period"
    )
    parser.add_argument(
        "--example", 
        action="store_true",
        help="Show usage example"
    )

    args = parser.parse_args()

    if args.example:
        print("\nExample usage:")
        print("python wagner_whitin_cli.py -d 172,183,173,233,229,239,257,251,650,636,662,674,643 -s 1745 -c 2.52")
        print("\nThis example matches the example data in the GUI version.")
        return

    # Input validation
    if not args.demand:
        print("Error: Demand list cannot be empty.")
        return

    if any(d < 0 for d in args.demand):
        print("Error: Demand values cannot be negative.")
        return

    if args.setup_cost < 0:
        print("Error: Setup cost cannot be negative.")
        return
    
    if args.holding_cost < 0:
        print("Error: Holding cost cannot be negative.")
        return

    # Create arrays for setup cost and holding cost
    num_periods = len(args.demand)
    setup_cost = [args.setup_cost] * num_periods
    holding_cost = [args.holding_cost] * num_periods

    # Print input summary
    print("\n--- Input Summary ---")
    print(f"Number of periods: {num_periods}")
    print(f"Total demand: {sum(args.demand):.2f}")
    print(f"Setup cost per period: {args.setup_cost:.2f}")
    print(f"Holding cost per unit per period: {args.holding_cost:.2f}")

    print("\nCalculating Wagner-Whitin plan...")
    
    try:
        min_cost, schedule, detailed_plan = wagner_whitin(args.demand, setup_cost, holding_cost)

        print("\n--- Results ---")
        print(f"Minimum total cost: {min_cost:.2f}")
        
        if schedule:
            print("Order schedule (1-indexed periods): " + ", ".join(map(str, schedule)))
        else:
            print("Order schedule: No orders needed or plan not found.")

        print("\nDetailed Order Plan:")
        for line in detailed_plan:
            print(line)

    except Exception as e:
        print(f"An error occurred during calculation: {e}")


if __name__ == "__main__":
    main()