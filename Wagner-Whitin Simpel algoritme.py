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


if __name__ == "__main__":
    # Example usage
    demand = [20, 0, 30, 10, 20, 30, 50, 23, 1435, 13, 13, 244, 11, 23, 12, 23, 12, 23, 12, 23, 12, 23, 12, 23, 33, 12, 1999, 34, 3243, 35, 12, 34, 76, 45, 344, 144, 122,]
    setup = [100] * len(demand)  # Fixed ordering cost for each period
    holding = [2] * len(demand) # Fixed Holding cost for each period

    C, order_period, schedule = wagner_whitin(demand, setup, holding)
    print("Minimum total cost:", C[len(demand)])
    print("Order schedule (order periods):", schedule)
