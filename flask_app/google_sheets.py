import gspread
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_students(students_sheets):
    # Get all the data from the sheet
    data = students_sheets.get_all_values()

    # Extract the header and rows
    header = data[0]
    rows = data[1:]

    # Create the dictionaries
    agent_conflicts = {}
    agent_capacities = {}
    agent_budgets = {}

    for row in rows:
        student = row[0]
        capacity = int(row[1])
        budget = float(row[2])
        conflicts = row[3].split(',') if row[3] else []

        agent_capacities[student] = capacity
        agent_budgets[student] = budget
        agent_conflicts[student] = conflicts

    return agent_conflicts, agent_capacities, agent_budgets


def get_valuations(valuations_sheets):
    data = valuations_sheets.get_all_values()
    # Extract the header and rows
    header = data[0]
    rows = data[1:]

    # Create the dictionary
    valuations = {}
    for row in rows:
        name = row[0]
        valuations[name] = {}
        for i, course in enumerate(header[1:]):
            valuations[name][course] = int(row[i + 1])

    return valuations


def get_courses(courses_sheets):
    data = courses_sheets.get_all_values()

    # Extract the header and rows
    header = data[0]
    rows = data[1:]

    # Create the dictionaries
    item_conflicts = {}
    item_capacities = {}

    for row in rows:
        course = row[0]
        capacity = int(row[1])
        conflicts = row[2].split(',') if row[2] else []

        item_capacities[course] = capacity
        item_conflicts[course] = conflicts

    return item_capacities, item_conflicts 


def get_google_sheets_data():
    account = gspread.service_account("credentials.json")

    spreadsheet = account.open_by_url(os.getenv("GOOGLE_SHEETS_URL")) 


    students_sheets = spreadsheet.worksheet("Students")  
    courses_sheets = spreadsheet.worksheet("Courses")  
    valuations_sheets = spreadsheet.worksheet("Valuations")  

    item_capacities, item_conflicts = get_courses(courses_sheets)

    valuations = get_valuations(valuations_sheets)

    agent_conflicts, agent_capacities, agent_budgets = get_students(students_sheets)

    return item_capacities, item_conflicts, valuations, agent_conflicts, agent_capacities, agent_budgets
    # print(f"item_capacities: {item_capacities}, item_conflicts: {item_conflicts}")
    # print(f"valuations: {valuations}")
    # print(f"agent_conflicts: {agent_conflicts}, agent_capacities: {agent_capacities}, agent_budgets: {agent_budgets}")


def update_results_google_sheets(res, agent_budgets):

    account = gspread.service_account("credentials.json")

    spreadsheet = account.open_by_url(os.getenv("GOOGLE_SHEETS_URL"))
    output_sheets = spreadsheet.worksheet("Output")
    
    values = []
    for student in agent_budgets:
        row = [student] + res[student]
        values.append(row)
    # # Prepare data for update
    # values = []
    # for student, courses in res.items():
    #     row = [student] + courses
    #     values.append(row)
    
    output_sheets.clear()
    
    output_sheets.update(range_name='A2', values=values)


