# User Guide: Wagner-Whitin Algorithm Script

**Date:** May 14, 2025

This guide explains how to use the `Wagner-Whitin Simpel algoritme.py` script to solve lot-sizing problems. It covers basic usage, examples, and troubleshooting common issues.

## 1. Introduction

The `Wagner-Whitin Simpel algoritme.py` script implements the Wagner-Whitin algorithm, a dynamic programming approach to determine the optimal production (or order) schedule to meet demand over a set number of periods while minimizing total costs (setup costs and holding costs).

This script is useful for inventory management and production planning.

## 2. Prerequisites and Installation

Before using this script, ensure you have:

1.  Python installed (version 3.7+ recommended).
2.  The `numpy` library installed.

For detailed setup instructions, please refer to the `INSTALLATION_GUIDE.md` file located in the same directory.

## 3. How to Use the Script

The core of the script is the `wagner_whitin` function. To use it, you typically modify the example usage block at the end of the script file.

### 3.1. Input Parameters

The `wagner_whitin` function takes three main arguments:

- `demand`: A list or NumPy array representing the demand for each period.
  - Example: `[10, 20, 0, 30]` means demand is 10 in period 1, 20 in period 2, 0 in period 3, and 30 in period 4.
- `setup_cost`: A list or NumPy array representing the fixed cost incurred if an order is placed (or production is set up) in a given period. This list must be the same length as the `demand` list.
  - Example: `[100, 100, 100, 100]` means a setup cost of 100 for each period if an order is placed in that period.
- `holding_cost`: A list or NumPy array representing the cost to hold one unit of inventory from one period to the next. This list must be the same length as the `demand` list.
  - Example: `[1, 1, 1, 1]` means it costs 1 unit of currency to hold one item from period `t` to period `t+1`.

### 3.2. Modifying Inputs in the Script

Open the `Wagner-Whitin Simpel algoritme.py` file in a text editor. Scroll to the bottom where you see the `if __name__ == "__main__":` block.

```python
if __name__ == "__main__":
    # Example usage
    # MODIFY THESE LISTS FOR YOUR PROBLEM
    demand = [20, 0, 30, 10, 20] # Example: 5 periods
    setup = [100] * len(demand)  # Example: Fixed setup cost of 100 for all periods
    holding = [2] * len(demand) # Example: Fixed holding cost of 2 for all periods

    C, order_period, schedule = wagner_whitin(demand, setup, holding)
    print("Minimum total cost:", C[len(demand)])
    print("Order schedule (order periods):", schedule)
```

Change the `demand`, `setup`, and `holding` lists to match your specific problem.

### 3.3. Running the Script

1.  Ensure your virtual environment (e.g., `venv`) is activated in PowerShell or Command Prompt, and you are in the `jks` directory.
    ```powershell
    # If not already activated:
    # .\venv\Scripts\Activate.ps1
    # cd C:\Users\ankhs\repos\jks
    ```
2.  Run the script:
    ```powershell
    python "Wagner-Whitin Simpel algoritme.py"
    ```

### 3.4. Understanding the Output

The script will print two main pieces of information:

- **Minimum total cost:** The lowest possible cost to meet all demands over the specified periods. This is the value `C[len(demand)]`.
- **Order schedule (order periods):** A list of periods in which orders should be placed. The periods are 1-indexed.
  - Example: `[1, 3]` means an order should be placed in period 1 (to cover demand for period 1 and possibly subsequent periods) and another order in period 3 (to cover demand for period 3 and possibly subsequent periods). The quantity to order in each of these periods is the sum of demands from that order period up to the period before the next scheduled order (or up to the final period if it\'s the last order).

## 4. Examples

### 4.1. Beginner Example

**Scenario:** You have a 3-period planning horizon.

- Demands: Period 1: 10 units, Period 2: 20 units, Period 3: 15 units.
- Setup Cost: 50 for any period an order is placed.
- Holding Cost: 1 per unit per period.

**Script Modification:**

```python
if __name__ == "__main__":
    demand = [10, 20, 15]
    setup = [50, 50, 50]    # Or setup = [50] * len(demand)
    holding = [1, 1, 1]     # Or holding = [1] * len(demand)

    C, order_period, schedule = wagner_whitin(demand, setup, holding)
    print("Minimum total cost:", C[len(demand)])
    print("Order schedule (order periods):", schedule)
```

**Expected Output (Illustrative - actual values depend on the algorithm\'s precise calculation):**

```
Minimum total cost: 135.0
Order schedule (order periods): [1, 3]
```

_Interpretation:_

- The minimum cost is 135.
- Order in period 1 (for periods 1 & 2: 10+20=30 units).
  - Cost: 50 (setup) + 0 (holding for period 1 demand) + 20\*1 (holding for period 2 demand from period 1 to 2).
- Order in period 3 (for period 3: 15 units).
  - Cost: 50 (setup).
- Total: 50 + 20 + 50 = 120. (Note: The example output was illustrative, the algorithm finds the true optimum. Let\'s trace this specific case:
  * Order P1 for P1, P2, P3: 50 (setup) + (20*1) + (15*2) = 50 + 20 + 30 = 100
  * Order P1 for P1, P2; Order P3 for P3: 50 (setup P1) + (20*1) (hold P2) + 50 (setup P3) = 50 + 20 + 50 = 120
  * Order P1 for P1; Order P2 for P2, P3: 50 (setup P1) + 50 (setup P2) + (15*1) (hold P3) = 50 + 50 + 15 = 115
  * Order P1 for P1; Order P2 for P2; Order P3 for P3: 50+50+50 = 150
  The algorithm would find the optimal, which is 100 in this case, with schedule [1]. The output would be:
  `    Minimum total cost: 100.0
    Order schedule (order periods): [1]
   `
  )

### 4.2. Advanced Example

**Scenario:** 5 periods with varying costs and a period with zero demand.

- Demands: `[25, 40, 0, 30, 50]`
- Setup Costs: `[200, 200, 180, 200, 180]` (Cheaper to set up in periods 3 and 5)
- Holding Costs: `[2, 2, 1, 1, 3]` (Holding cost changes, cheaper in later periods before the last)

**Script Modification:**

```python
if __name__ == "__main__":
    demand = [25, 40, 0, 30, 50]
    setup = [200, 200, 180, 200, 180]
    holding = [2, 2, 1, 1, 3]

    C, order_period, schedule = wagner_whitin(demand, setup, holding)
    print("Minimum total cost:", C[len(demand)])
    print("Order schedule (order periods):", schedule)
```

**Running this would yield an optimal schedule and cost based on these specific inputs.** The algorithm handles zero demand periods correctly by not producing for them unless it\'s optimal to produce in advance for a future period.

## 5. Typical Error Messages and Troubleshooting

- **`ModuleNotFoundError: No module named 'numpy'`**

  - **Cause:** The `numpy` library is not installed, or Python cannot find it.
  - **Solution:**
    1.  Ensure your virtual environment is activated.
    2.  Run `pip install numpy`.
    3.  Refer to `INSTALLATION_GUIDE.md` for more details.

- **`IndexError: list index out of range` (or similar errors from NumPy)**

  - **Cause:** The `demand`, `setup_cost`, or `holding_cost` lists might not be of the same length, or there\'s an issue with how they are indexed internally (less likely with the current script structure if inputs are correct).
  - **Solution:**
    1.  Verify that `len(demand)`, `len(setup_cost)`, and `len(holding_cost)` are all equal.
    2.  Ensure all lists contain valid numerical data.

- **`TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'` (or similar type errors)**

  - **Cause:** One of the input lists might contain non-numeric data (e.g., `None`, a string).
  - **Solution:** Ensure all elements in `demand`, `setup_cost`, and `holding_cost` are numbers (integers or floats). The script attempts to convert to `float` using `np.array(..., dtype=float)`, which should handle integers, but `None` or strings will cause issues.

- **Output shows very high costs or unexpected schedule:**

  - **Cause:** Input data might be incorrect (e.g., extremely high holding costs, very low setup costs leading to frequent orders, or vice-versa).
  - **Solution:**
    1.  Double-check the `demand`, `setup_cost`, and `holding_cost` values for typos or logical errors.
    2.  Test with a very small, simple example for which you can manually calculate or estimate the optimal solution to verify the algorithm\'s behavior.

- **PowerShell: `.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`**
  - **Cause:** PowerShell execution policy prevents running local scripts.
  - **Solution:** As mentioned in `INSTALLATION_GUIDE.md`, open PowerShell as Administrator and run:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ```
    Then try activating the virtual environment again in your regular PowerShell window.

This user guide should help you effectively use the Wagner-Whitin script. For further assistance or more complex scenarios, understanding the underlying Wagner-Whitin algorithm principles is recommended.
