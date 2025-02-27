"""
Title: Task Tracker
Date: 10/02/2025
Author: Azariah Pundari (aztec-dev)
"""
import json
import os
from datetime import date

FILE_NAME = 'tasks.json'

# task object placeholder.
tasks = []

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
            task_name = option[4:]  # Extract task name
            add_task(FILE_NAME, task_name)
        elif option.startswith("update "):
            task_id = option[7:8]  # Extract task ID
            updated_task = option[9:]
            update_task(FILE_NAME, task_id, updated_task)
            # print(task_id)
            # print(updated_task)
        option = input("task-cli ")
    print("exit")

def add_task(file_name, task_name):
    """
    Adds a task to tasks.json based on user input
    
    Parameters:
    file_name (str): Name of the file to write data to.
    task_name (str): Name of the task.

    Returns:
    NA
    prints a status message.
    """
    status = validate_file(file_name)
    data = read_data(file_name)
    data.append({"id": len(data) + 1, "task": task_name, "createdAt": date.today().isoformat()})
    if status:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        pass
    print(f"Task added successfully (ID: {len(data)})")

def update_task(file_name, task_id, updated_task):
    """
    Updates a task based on the task ID provided by the user.

    Parameters:
    file_name (string): Represents the file path
    task_id (int): Represents the task ID
    """
    status = validate_file(file_name)
    data = read_data(file_name)
    task_offset = int(task_id) - 1
    stripped_task = updated_task.strip('"')
    data[task_offset].update({"task": stripped_task,"updatedAt": date.today().isoformat()})
    if status:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

def list_tasks(file_name:str):
    """
    Reads from the file and lists the tasks.
    
    Parameters:
    file_name (str): Name of the file to read/display data from.

    Returns:
    prints a string.
    """
    # Validate the file
    status = validate_file(file_name)
    # Read the data
    data = read_data(file_name) 
    if status and len(data) != 0:
        # print(len(data))
        for task in data:
            print(f'{task["id"]}: {task["task"]}')
    else:
        print("You haven't added any tasks yet.")

def validate_file(file_name:str):
    """
    Validates the files existence and validates the data in the file.
    Creates file if it doesn't exists.
    Parameters:
    file_name (str): Name of the file to be validated.

    Returns:
    bool: True if the file is a valid file.
    """
    # Check if the file exists and is not empty.
    if os.path.exists(file_name):
        return True
    else:
        create_file(file_name, tasks)
        return True
    
def read_data(file_name:str):
    """
    Read the data from a file
    
    Parameters:
    file_name (str): Name of the .json file to be validated

    Returns:
    object (dict): Data read from .json file
    """
    status = validate_file(file_name)
    if status:
        with open(file_name, 'r') as outfile:
            data = json.load(outfile)
    return data

def create_file(file_name:str, default_struct:dict):
    """
    Creates a new file containing a default structure to store data.

    Parameters:
    file_name (str): Name of the file to be validated.

    Returns:
    list: An empty list that is written into the new file.
    """
    with open(file_name, 'w') as file:
        data = json.dump(default_struct, file, indent=4)
    return data
main()