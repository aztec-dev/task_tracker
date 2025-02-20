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
    "id": 0,
    "task": "placeholder",
    "status" : "placeholder",
    "createdAt": "placeholder",
    "updatedAt": "placeholder",
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
            list_tasks(FILE_NAME)
        elif option.startswith("add "):
            task_name = option[4:]  # Extracts task
            tasks["task"] = task_name
            add_task(FILE_NAME, tasks)
        option = input("task-cli ")
    print("exit")

def add_task(file_name, json_object):
    """Adds a task to tasks.json based on user input"""
    status, data = validate_file(file_name)
    if status == True:
        json_object["id"] += 1
        data.append(json_object)
    else:
        create_file(file_name)
        data.append(json_object)
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    print(f"Task added successfully (ID: {json_object["id"]})")

def list_tasks(file_name):
    """Reads from the file and lists the tasks."""
    status, data = validate_file(file_name)
    if status == True and len(data) != 0:
        for task in data:
            print(f'{task["id"]}: {task["task"]}')
    elif len(data) == 0:
        print("You haven't added any tasks yet.")


def validate_file(file_name):
    """Validates the files existence and validates the data in the file."""
    # Check if the file exists
    if os.path.exists(file_name):
        # Check if file is not empty
        if os.path.getsize(file_name) != 0:
            with open(file_name, 'r') as infile:
                data = json.load(infile)
            return True, data
        else:
            new_data = create_file(file_name)
            return True, new_data
    else:
        # Create a new file and populate it with an empty array.
        new_data = create_file(file_name)
        return True, new_data

def create_file(file_name):
    """Creates a new file containing an empty array."""
    data = []
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)
    return data

main()