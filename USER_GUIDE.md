# User Guide: Wagner-Whitin Algorithm Script & Web UI

**Date:** May 14, 2025

This guide explains how to use the `wagner_whitin_simple_algoritme.py` script and its associated web interface to solve lot-sizing problems. It covers usage for both the command-line interface (CLI) and the web UI, examples, and troubleshooting.

## 1. Introduction

The `wagner_whitin_simple_algoritme.py` script implements the Wagner-Whitin algorithm, a dynamic programming approach to determine the optimal production (or order) schedule to meet demand over a set number of periods while minimizing total costs (setup costs and holding costs).

This project provides two ways to interact with the algorithm:

- **Command-Line Interface (CLI):** Directly run the Python script and input data via prompts.
- **Web-based Graphical User Interface (Web UI):** Start a local web server to input data and see results in your browser.

This tool is useful for inventory management and production planning.

## 2. Prerequisites and Installation

Before using this script or web UI, ensure you have:

1. Python installed (version 3.7+ recommended).
2. The necessary Python packages installed. These are listed in `requirements.txt`.

For detailed setup instructions, including how to set up a virtual environment and install dependencies from `requirements.txt` (which includes `numpy` and `Flask`), please refer to the `INSTALLATION_GUIDE.md` file located in the same directory.

## 3. How to Use the Script

You can interact with the Wagner-Whitin algorithm either through the CLI or the Web UI.

### 3.1. Using the Command-Line Interface (CLI)

The CLI allows you to run the script directly in your terminal and input data interactively.

**Steps:**

1. **Activate Virtual Environment:**
   Open PowerShell or Command Prompt, navigate to your project directory (`C:\Users\ankhs\repos\jks\`), and activate the virtual environment:

   ```powershell
   # In PowerShell
   .\venv\Scripts\Activate.ps1
   ```

   ```cmd
   # In Command Prompt
   .\venv\Scripts\activate.bat
   ```

2. **Run the Script:**
   Execute the script using Python:

   ```powershell
   python wagner_whitin_simple_algoritme.py
   ```

3. **Interactive Input:**
   The script will guide you through the input process:

   - **Use example data?**: You'll first be asked if you want to use predefined example data. Type `yes` or `no`.
     - If `yes`, the script runs with a built-in example.
     - If `no`, you'll be prompted to enter your own data:
       - **Number of periods (T):** Enter the total number of periods for your planning horizon (e.g., `5`).
       - **Demand for each period:** For each period `i`, enter the demand `d_i`.
       - **Setup cost for each period:** For each period `i`, enter the setup cost `K_i`.
       - **Holding cost for each period:** For each period `i`, enter the holding cost `h_i` (cost to hold one unit from period `i` to `i+1`).

**CLI Output:**

After providing all inputs, the script will print:

- **Minimum total cost:** The lowest possible cost.
- **Order schedule (periods to place orders - 1-indexed):** A comma-separated list of periods in which orders should be placed.
- **Detailed Order Plan:** For each order period, the quantity to produce and the range of demand periods it covers.

**Example CLI Interaction:**

```text
Wagner-Whitin Lot Sizing Calculator
-----------------------------------
Do you want to use the predefined example data? (yes/no): no

Enter data for the lot-sizing problem:
Enter the number of periods (T): 3

Enter details for each period:
--- Period 1 ---
  Demand for period 1: 10
  Setup cost for period 1: 50
  Holding cost for period 1 (per unit from 1 to 2): 1
--- Period 2 ---
  Demand for period 2: 20
  Setup cost for period 2: 50
  Holding cost for period 2 (per unit from 2 to 3): 1
--- Period 3 ---
  Demand for period 3: 15
  Setup cost for period 3: 50
  Holding cost for period 3 (per unit from 3 to 4): 1
-----------------------------------

Calculating optimal schedule...

--- Results ---
Minimum total cost: 100.00
Order schedule (periods to place orders - 1-indexed): 1
Detailed Order Plan:
  Order in Period 1: Produce 45.00 units (to cover demand for periods 1 to 3)
-----------------------------------
```

### 3.2. Using the Web-based Graphical User Interface (Web UI)

The Web UI provides a user-friendly way to input data and view results in your web browser. It uses Flask as a backend.

**Steps:**

1. **Activate Virtual Environment:**
   Ensure your virtual environment is active (see step 1 in section 3.1).

2. **Start the Flask Web Server:**
   In your terminal (PowerShell or Command Prompt), navigate to the project directory (`C:\Users\ankhs\repos\jks\`) and run the `app.py` file:

   ```powershell
   python app.py
   ```

   You should see output indicating the server is running, typically on `http://127.0.0.1:5000/`.

   ```text
   * Serving Flask app 'app'
   * Debug mode: off
   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
   ```

3. **Open in Browser:**
   Open your web browser (e.g., Chrome, Firefox, Edge) and go to the address: `http://127.0.0.1:5000/`

4. **Input Data via Web Form:**
   The web page will display a form with the following fields:

   - **Demand per period (comma-separated):** Enter demands for each period, separated by commas (e.g., `10,20,0,30`).
   - **Setup cost per period (comma-separated):** Enter setup costs for each period, separated by commas (e.g., `100,100,100,100`).
   - **Holding cost per period (comma-separated):** Enter holding costs for each period, separated by commas (e.g., `1,1,1,1`).

   Ensure you enter the same number of values in each field.

5. **Calculate and View Results:**
   Click the "Calculate Optimal Schedule" button. The results (minimum total cost and order schedule) will be displayed below the form. If there are errors (e.g., mismatched number of inputs), an error message will appear.

**Web UI Output:**

The results section will show:

- **Minimum Total Cost:** The calculated optimal cost.
- **Order Schedule (Periods):** A list of periods in which to place orders.

### 3.3. Input Parameters (Core Algorithm)

The underlying `wagner_whitin` function (used by both CLI and Web UI) takes three main arguments:

- `demand`: A list or NumPy array representing the demand for each period.
- `setup_cost`: A list or NumPy array representing the fixed cost incurred if an order is placed in a given period. Must be the same length as `demand`.
- `holding_cost`: A list or NumPy array representing the cost to hold one unit of inventory from one period to the next. Must be the same length as `demand`.

## 4. Examples

### 4.1. Example 1: Simple 3-Period Scenario

**Scenario:**

- Periods: 3
- Demands: `[10, 20, 15]`
- Setup Costs: `[50, 50, 50]` (or `50` for all periods)
- Holding Costs: `[1, 1, 1]` (or `1` for all periods)

**Using the CLI:**

Follow the prompts as shown in section 3.1, entering the data above.
Expected Output:

```text
Minimum total cost: 100.00
Order schedule (periods to place orders - 1-indexed): 1
Detailed Order Plan:
  Order in Period 1: Produce 45.00 units (to cover demand for periods 1 to 3)
```

**Using the Web UI:**

1. Start `app.py`.
2. Open `http://127.0.0.1:5000/`.
3. Input:
   - Demand: `10,20,15`
   - Setup cost: `50,50,50`
   - Holding cost: `1,1,1`
4. Click "Calculate".

Expected Output on Web Page:

- Minimum Total Cost: 100.0
- Order Schedule (Periods): `[1]`

### 4.2. Example 2: 5 Periods with Zero Demand and Varying Costs

**Scenario:**

- Periods: 5
- Demands: `[25, 40, 0, 30, 50]`
- Setup Costs: `[200, 200, 180, 200, 180]`
- Holding Costs: `[2, 2, 1, 1, 3]`

**Using the CLI:**

Enter `no` for example data, then `5` for periods, and then input the lists above when prompted.

**Using the Web UI:**

1. Start `app.py`.
2. Open `http://127.0.0.1:5000/`.
3. Input:
   - Demand: `25,40,0,30,50`
   - Setup cost: `200,200,180,200,180`
   - Holding cost: `2,2,1,1,3`
4. Click "Calculate".

The output for both methods will show the optimal cost and schedule for this specific scenario. The algorithm correctly handles zero demand periods.

## 5. Typical Error Messages and Troubleshooting

- **`ModuleNotFoundError: No module named 'numpy'` or `No module named 'flask'`**

  - **Cause:** Required libraries are not installed, or Python cannot find them.
  - **Solution:**
    1. Ensure your virtual environment is activated.
    2. Run `pip install -r requirements.txt` in your project directory.
    3. Refer to `INSTALLATION_GUIDE.md` for more details.

- **CLI: `Invalid input. Please enter a number/integer.`**

  - **Cause:** You entered non-numeric text when a number was expected.
  - **Solution:** Re-enter a valid number.

- **Web UI: Error message "Number of items in demand, setup costs, and holding costs must be the same."**

  - **Cause:** The comma-separated lists entered into the web form do not have the same number of elements.
  - **Solution:** Correct the input fields so that `demand`, `setup_cost`, and `holding_cost` all have an equal number of comma-separated values.

- **Web UI: Error message "Invalid input: All values must be numbers."**

  - **Cause:** One or more values in the comma-separated lists are not valid numbers.
  - **Solution:** Ensure all entries are numeric.

- **`IndexError: list index out of range` (or similar errors from NumPy in CLI)**

  - **Cause:** This is less likely with the interactive CLI if inputs are entered as prompted. If modifying the script directly, it could mean `demand`, `setup_cost`, or `holding_cost` lists are not of the same length.
  - **Solution:**
    1. If using CLI, ensure you complete all prompts correctly.
    2. If modifying script code, verify that `len(demand)`, `len(setup_cost)`, and `len(holding_cost)` are all equal.

- **`TypeError: unsupported operand type(s)` (CLI)**

  - **Cause:** Input lists might contain non-numeric data if the script was modified or if there's a bug in input handling (less likely with current `get_numeric_input`).
  - **Solution:** Ensure all data provided are numbers.

- **Output shows very high costs or unexpected schedule:**

  - **Cause:** Input data might be incorrect (e.g., typos, extremely high holding costs, very low setup costs leading to frequent orders, or vice-versa).
  - **Solution:**
    1. Double-check the `demand`, `setup_cost`, and `holding_cost` values for typos or logical errors.
    2. Test with a very small, simple example for which you can manually calculate or estimate the optimal solution.

- **PowerShell: `.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`**

  - **Cause:** PowerShell execution policy prevents running local scripts.
  - **Solution:** As mentioned in `INSTALLATION_GUIDE.md`, open PowerShell as Administrator and run:

    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ```

    Then try activating the virtual environment again in your regular PowerShell window.

- **Web UI: Flask server (`app.py`) doesn't start or shows errors.**
  - **Cause:** Could be various issues: Flask not installed, port already in use, syntax errors in `app.py` or `wagner_whitin_simple_algoritme.py`.
  - **Solution:**
    1. Ensure Flask is installed (`pip install -r requirements.txt`).
    2. Check the terminal output for specific error messages when you run `python app.py`.
    3. If the port is in use, Flask will usually indicate this. You might need to stop the other process or modify `app.py` to use a different port (e.g., `app.run(debug=True, port=5001)`).

This user guide should help you effectively use the Wagner-Whitin script and web interface.
