"""
Title: Task Tracker
Date: 10/02/2025
Author: Azariah Pundari (aztec-dev)
"""
import json
import os

FILE_NAME = 'tasks.json'

tasks = {
    "id": "1",
    "description": "sample task",
    "status" : "status",
    "createdAt": "created at",
    "updatedAt": "updated at"
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
            print(open_tasks(FILE_NAME))
        elif option == f"add {task_name}":
            while task_name == "":
                print("Incorrect task name")
        option = input("task-cli ")
    print("exit")

def open_tasks(file_name):
    """Displays a list of the current tasks within the file."""
    # Check if file exists, if not => opens a readable file.
    if not os.path.exists(file_name):
        with open(file_name, "r") as task_file:
            # Display data
            data = json.load(task_file)
            return data

main()