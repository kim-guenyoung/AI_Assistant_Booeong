from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)

def get_menu_items(day_of_week, meal_type="single", is_student=True):
    # Define the menu orders based on the meal type
    menu_orders = {
        "breakfast": {
            0: [1],
            1: [2],
            2: [3],
            3: [4],
            4: [5],
            5: [], 
            6: []
        },
        "single": {
            0: [6],
            1: [7],
            2: [8],
            3: [9],
            4: [10],
            5: [],  # Saturday, no menu
            6: []   # Sunday, no menu
        },
        "baekban": {
            0: [11],
            1: [12],
            2: [13],
            3: [14],  # Add 14 for Thursday
            4: [],
            5: [],  # Saturday, no menu
            6: []   # Sunday, no menu
        },
        "faculty": {
            0: [1],
            1: [2],
            2: [3],
            3: [4],
            4: [5],
            5: [],  # Saturday, no menu
            6: []   # Sunday, no menu
        }
    }

    # Choose the appropriate menu order based on the meal type
    menu_order = menu_orders.get(meal_type, {})

    # Get the menu items for the current day
    return menu_order.get(day_of_week, [])

@app.route('/')
def display_menu():
    try:
        # For testing purposes, assuming today is Wednesday (2)
        today = datetime.now().weekday()
        # today = 4
        # Read student menu data from the JSON file
        with open('menu_student.json', 'r') as student_file:
            student_menu_data = json.load(student_file)

        # Read faculty menu data from the JSON file
        with open('menu_faculty.json', 'r') as faculty_file:
            faculty_menu_data = json.load(faculty_file)

        # Get the menu items for the current day for different meal types
        breakfast_menu_items = get_menu_items(today, meal_type="breakfast")
        single_menu_items = get_menu_items(today, meal_type="single")
        baekban_menu_items = get_menu_items(today, meal_type="baekban")
        faculty_menu_items = get_menu_items(today, meal_type="faculty", is_student=False)

        # Create lists of menu items to display for each meal type
        breakfast_menu_to_display = [student_menu_data[item - 1] for item in breakfast_menu_items]
        single_menu_to_display = [student_menu_data[item - 1] for item in single_menu_items]
        baekban_menu_to_display = [student_menu_data[item - 1] for item in baekban_menu_items]
        faculty_menu_to_display = [faculty_menu_data[item - 1] for item in faculty_menu_items]

        # Render the template with menu data for each meal type
        return render_template('menu_template.html',
                               breakfast_menu_data=breakfast_menu_to_display,
                               single_menu_data=single_menu_to_display,
                               baekban_menu_data=baekban_menu_to_display,
                               faculty_menu_data=faculty_menu_to_display)

    except Exception as e:
        # Handle errors
        return f"오류 발생: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
