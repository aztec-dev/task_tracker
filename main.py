"""
Title: Task Tracker
Date: 10/02/2025
Author: Azariah Pundari (aztec-dev)
"""
import json
import os

FILE_NAME = 'tasks.json'

# task object placeholder.
tasks = {
    "id": None,
    "description": None,
    "status" : None,
    "createdAt": None,
    "updatedAt": None,
}

tasks_to_json = json.dumps(tasks, indent=4)
MENU = "add [task name/description] => adds a new task\n\
update [ID] => updates a task based on ID\n\
delete [ID] => deletes a task based on ID\n\
list [status] => list all tasks based on status\n"


def main():
    """Main program."""
    print(MENU)

    option = input("task-cli ")
    task_name = ""

    while option != "exit":
        if option == "list":
            print(list_tasks(FILE_NAME))
        elif option == f"add {task_name}":
            while task_name == "":
                print("Incorrect task name")
        option = input("task-cli ")
    print("exit")

def list_tasks(file_name):
    """Displays a list of the current tasks within the file."""
    # Check if file exists, if not => creates a read/write file.
    with open(file_name, 'r') as out_file:
        content = out_file.read()
        if content.strip():
            parsed_data = json.load(out_file)
            return parsed_data
        else:
            return "No task to display. Consider running [add] to add a task."

main()