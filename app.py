from flask import Flask, render_template, request, jsonify
import numpy as np
import sys
import os

# Add the directory of the script to the Python path
# to ensure 'wagner_whitin_simple_algoritme' can be imported
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from wagner_whitin_simple_algoritme import wagner_whitin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        demand_str = data.get('demand', [])
        setup_cost_str = data.get('setup_cost', [])
        holding_cost_str = data.get('holding_cost', [])

        # Convert string inputs to lists of floats
        # Assuming inputs are comma-separated strings or lists of numbers
        def parse_input_list(input_val):
            if isinstance(input_val, str):
                return [float(x.strip()) for x in input_val.split(',') if x.strip()]
            elif isinstance(input_val, list):
                return [float(x) for x in input_val]
            return []

        demand = parse_input_list(demand_str)
        setup_cost = parse_input_list(setup_cost_str)
        holding_cost = parse_input_list(holding_cost_str)

        if not (len(demand) == len(setup_cost) == len(holding_cost)):
            return jsonify({'error': 'Demand, setup costs, and holding costs must have the same number of periods.'}), 400
        
        if not demand:
             return jsonify({'error': 'Input data cannot be empty.'}), 400

        C, order_period, schedule = wagner_whitin(demand, setup_cost, holding_cost)

        # Convert numpy array to list for JSON serialization
        min_cost = C[len(demand)] if isinstance(C, np.ndarray) and len(C) > len(demand) else C[-1] if isinstance(C, np.ndarray) else C

        return jsonify({
            'min_total_cost': min_cost,
            'order_schedule': schedule
        })

    except ValueError as e:
        return jsonify({'error': f'Invalid input data: {str(e)} Please ensure all inputs are numbers.'}), 400
    except Exception as e:
        app.logger.error(f"Calculation error: {e}", exc_info=True)
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # It's good practice to rename "Wagner-Whitin Simpel algoritme.py"
    # to something like "wagner_whitin_logic.py" for easier imports.
    # If you do, update the import statement at the top.
    print("Attempting to import Wagner-Whitin logic...")
    print(f"Looking for 'Wagner-Whitin Simpel algoritme.py' or similar in {script_dir}")
    app.run(debug=True)
