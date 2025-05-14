# Wagner-Whitin Lot Sizing Calculator

This application calculates the optimal lot-sizing schedule using the Wagner-Whitin algorithm to minimize total costs (setup and holding costs) over a defined number of periods.

## How to Run

1.  Ensure you have Python installed.
2.  Install the necessary libraries:
    ```bash
    pip install numpy dearpygui
    ```
3.  Navigate to the `jks` directory in your terminal.
4.  Run the application using the following command:
    ```bash
    python wagner_whitin_simple_algoritme.py
    ```

## Usage

The application window will open, presenting the following input fields and controls:

### Input Fields

*   **Demand (comma-separated):**
    *   Enter the demand for each period, separated by commas.
    *   Example: `20, 0, 30, 10, 50` (This represents demand for 5 periods).
    *   Demand values cannot be negative.
*   **Setup Cost (per period):**
    *   Enter a single fixed cost incurred each time an order is placed. This cost will be applied to any period an order is made.
    *   Example: `100`
    *   The setup cost cannot be negative.
*   **Holding Cost (per unit, per period):**
    *   Enter a single per-unit cost for holding one unit of inventory from one period to the next. This cost will be applied uniformly.
    *   Example: `2.5`
    *   The holding cost cannot be negative.

A `(?)` icon next to each input field provides a tooltip with an example.

### Controls

*   **Calculate Button:**
    *   After entering all required data, click this button to perform the Wagner-Whitin calculation.
    *   The results will be displayed below.
*   **Use Example Data Button:**
    *   Click this button to populate the input fields with pre-defined example values. This is useful for quickly seeing how the application works.
*   **Clear Inputs Button:**
    *   Click this button to clear all data from the input fields and reset the results and status messages.

### Output Section

*   **Status Text:**
    *   Displays the current status of the application (e.g., "Calculating...", "Calculation complete.", "Error: ..."). Error messages will appear here if inputs are invalid.
*   **Minimum total cost:**
    *   Shows the calculated minimum total cost to satisfy all demands according to the optimal plan.
*   **Order schedule:**
    *   Lists the 1-indexed periods in which orders should be placed.
    *   Example: `Order schedule (1-indexed periods): 1, 4` (means order in period 1 and period 4).
*   **Detailed Order Plan:**
    *   Provides a multi-line text area showing details for each order in the optimal schedule:
        *   The period in which the order is placed.
        *   The quantity to produce/order.
        *   The individual cost of that specific order (setup cost + holding costs for items from that order).
        *   The range of periods for which this order covers demand.
    *   Example: `Order in Period 1: Produce 60.00 units (Cost: 140.00) to cover demand for periods 1 to 3.`

## Error Handling

*   If the input data is not in the correct format (e.g., non-numeric values, incorrect comma separation), an error message will be displayed in the status area.
*   If logical errors are detected (e.g., negative demand, setup costs, or holding costs), specific error messages will guide you.
*   The application also checks if demand data is provided.

This should help you get started with the Wagner-Whitin Lot Sizing Calculator!
