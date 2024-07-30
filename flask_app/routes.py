from flask import Flask, render_template, jsonify
from flask_app import app
from flask_app.input_google_sheets import get_google_sheets_data, update_results_google_sheets

import fairpyx
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    try:
        # Get data from Google Sheets
        item_capacities, item_conflicts, valuations, agent_conflicts, agent_capacities, agent_budgets = get_google_sheets_data()
        
        # Run the course match algorithm
        instance = fairpyx.Instance(item_capacities=item_capacities, item_conflicts=item_conflicts, valuations=valuations, agent_conflicts=agent_conflicts, agent_capacities=agent_capacities)
        allocation = fairpyx.divide(algorithm=fairpyx.algorithms.iterated_maximum_matching, instance=instance)

        # Update Google Sheets with the results
        update_results_google_sheets(allocation)
        
        return jsonify({"status": "success", "message": "Algorithm executed successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500