import fairpyx.algorithms.course_match
import fairpyx.algorithms.course_match.main_course_match
from fairpyx.algorithms.course_match.A_CEEI import logger as ACEEI_logger
from fairpyx.algorithms.course_match.remove_oversubscription import logger as remove_oversubscription_logger
from fairpyx.algorithms.course_match.reduce_undersubscription import logger as reduce_undersubscription_logger 
import logging
from io import StringIO

from flask import Flask, render_template, jsonify
from flask_app import app
from flask_app.google_sheets import get_google_sheets_data, update_results_google_sheets

import fairpyx
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    try:
        
        log_stream = StringIO()    

        ACEEI_logger.setLevel(logging.INFO)
        ACEEI_logger.addHandler(logging.StreamHandler(log_stream))

        remove_oversubscription_logger.setLevel(logging.INFO)
        remove_oversubscription_logger.addHandler(logging.StreamHandler(log_stream))

        reduce_undersubscription_logger.setLevel(logging.INFO)
        reduce_undersubscription_logger.addHandler(logging.StreamHandler(log_stream))

        # Get data from Google Sheets
        item_capacities, item_conflicts, valuations, agent_conflicts, agent_capacities, agent_budgets = get_google_sheets_data()
     
        # Run the course match algorithm
        instance = fairpyx.Instance(item_capacities=item_capacities, item_conflicts=item_conflicts, valuations=valuations, agent_conflicts=agent_conflicts, agent_capacities=agent_capacities)

        allocation = fairpyx.divide(algorithm=fairpyx.algorithms.course_match.main_course_match.course_match_algorithm, instance=instance, budget=agent_budgets,time=5)

        update_results_google_sheets(allocation,agent_budgets)
        
        print(log_stream.getvalue())
        

        log_contents = log_stream.getvalue()

        return jsonify(log=log_contents)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500