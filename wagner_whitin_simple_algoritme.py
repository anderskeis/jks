import numpy as np

def wagner_whitin(demand, setup_cost, holding_cost):
    """
    Solves the Wagner-Whitin lot-sizing problem using dynamic programming.

    Parameters
    ----------
    demand : list or 1D-array of length T
        demand d_t for periods t = 1..T.
    setup_cost : list or 1D-array of length T
        fixed ordering cost K_t for each period.
    holding_cost : list or 1D-array of length T
        per-unit holding cost h_t for carrying inventory from t to t+1.

    Returns
    -------
    C : 1D-array of length T+1
        C[t] = minimum cost to satisfy demands up through period t.
    order_period : list of length T+1
        order_period[t] = the period j at which the order covering demand up to t was placed.
    schedule : list of periods
        list of order periods in optimal schedule.
    """
    T = len(demand)
    # Convert inputs to arrays for easier slicing
    d = np.array(demand, dtype=float)
    K = np.array(setup_cost, dtype=float)
    h = np.array(holding_cost, dtype=float)

    # Precompute holding cost matrix H[j, t]: cost to hold from j to cover demand through t
    H = np.zeros((T, T))
    for j in range(T):
        # cumulative demand from j+1 to each t
        for t in range(j+1, T):
            # sum over i=j to t-1 of h[i] * sum_{u=i+1 to t} d[u]
            cost = 0.0
            for i in range(j, t):
                cost += h[i] * d[i+1:t+1].sum()
            H[j, t] = cost

    # DP arrays
    C = np.full(T+1, np.inf)
    order_period = [-1] * (T+1)
    # base case
    C[0] = 0.0

    # Recurrence
    for t in range(1, T+1):
        for j in range(1, t+1):
            cost = C[j-1] + K[j-1]
            if j-1 < t-1:
                cost += H[j-1, t-1]
            if cost < C[t]:
                C[t] = cost
                order_period[t] = j

    # Backtrack to find schedule
    schedule = []
    t = T
    while t > 0:
        j = order_period[t]
        schedule.append(j)
        t = j - 1
    schedule.reverse()

    return C, order_period, schedule


def get_numeric_input(prompt_message):
    """Helper function to get and validate numeric input."""
    while True:
        try:
            value = float(input(prompt_message))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_integer_input(prompt_message, min_value=1):
    """Helper function to get and validate positive integer input."""
    while True:
        try:
            value = int(input(prompt_message))
            if value >= min_value:
                return value
            else:
                print(f"Please enter an integer greater than or equal to {min_value}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

if __name__ == "__main__":
    print("Wagner-Whitin Lot Sizing Calculator")
    print("-----------------------------------")

    use_example = input("Do you want to use the predefined example data? (yes/no): ").strip().lower()

    if use_example == 'yes':
        # Predefined example usage (as was originally in the script)
        demand = [20, 0, 30, 10, 20, 30, 50, 23, 1435, 13, 13, 244, 11, 23, 12, 23, 12, 23, 12, 23, 12, 23, 12, 23, 33, 12, 1999, 34, 3243, 35, 12, 34, 76, 45, 344, 144, 122,]
        setup = [100] * len(demand)  # Fixed ordering cost for each period
        holding = [2] * len(demand) # Fixed Holding cost for each period
        print("\nUsing predefined example data.")
    else:
        print("\nEnter data for the lot-sizing problem:")
        num_periods = get_integer_input("Enter the number of periods (T): ")

        demand = []
        setup = []
        holding = []

        print("\nEnter details for each period:")
        for i in range(num_periods):
            print(f"--- Period {i+1} ---")
            d_val = get_numeric_input(f"  Demand for period {i+1}: ")
            k_val = get_numeric_input(f"  Setup cost for period {i+1}: ")
            h_val = get_numeric_input(f"  Holding cost for period {i+1} (per unit from {i+1} to {i+2}): ")
            demand.append(d_val)
            setup.append(k_val)
            holding.append(h_val)
        print("-----------------------------------")

    if not demand: # Should not happen if logic is correct, but as a safeguard
        print("No data provided. Exiting.")
    else:
        print("\nCalculating optimal schedule...")
        C, order_period, schedule = wagner_whitin(demand, setup, holding)

        print("\n--- Results ---")
        print(f"Minimum total cost: {C[len(demand)]:.2f}")
        if schedule:
            print("Order schedule (periods to place orders - 1-indexed):", ", ".join(map(str, schedule)))
            # Optional: Print detailed order quantities
            print("\nDetailed Order Plan:")
            current_order_idx = 0
            for i in range(len(schedule)):
                order_in_period = schedule[i]
                start_period_idx = order_in_period -1 # 0-indexed
                
                if i + 1 < len(schedule):
                    # Order covers demand until the period before the next scheduled order
                    end_period_idx = schedule[i+1] - 2 # 0-indexed, period before next order
                else:
                    # Last order, covers demand until the end of the horizon
                    end_period_idx = len(demand) - 1 # 0-indexed
                
                quantity_to_order = sum(demand[k] for k in range(start_period_idx, end_period_idx + 1))
                print(f"  Order in Period {order_in_period}: Produce {quantity_to_order:.2f} units (to cover demand for periods {start_period_idx+1} to {end_period_idx+1})")
        else:
            print("No orders are needed (e.g., if demand is zero for all periods).")
        print("-----------------------------------")
