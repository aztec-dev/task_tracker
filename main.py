"""
Title: Task Tracker
Date: 10/02/2025
"""
import json
import os
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from datetime import datetime
from custom_id_generator import CustomIdGenerator
FILE_NAME = 'tasks.json'

# task object placeholder.
tasks = []
id_generator = CustomIdGenerator()

# cli style and input style
style = Style.from_dict({
    'prompt': 'bg:green fg:white', 
    '': 'fg:yellow'
})

MENU = "\033[33madd [task name/description]\033[0m => adds a new task\n\
\033[33mupdate [ID]\033[0m => updates a task based on ID\n\
\033[33mdelete [ID]\033[0m => deletes a task based on ID\n\
\033[33mlist [status]\033[0m => list all tasks based on status\n"


def main():
    """
    Behold, the program!
    """
    print(MENU)

    # option = input('task-cli ')
    option = prompt(
        [('class:propmt', 'task-cli '), ('class:input', '')],
        style=style,
    )

    while option != "exit":
        if option.startswith("list"):
            status = option[5:]  # Extract status
            list_tasks(FILE_NAME, status)
        elif option.startswith("add "):
            task_name = option[4:]  # Extract task name
            add_task(FILE_NAME, task_name)
        elif option.startswith("update "):
            task_id = option[7:8]  # Extract task ID
            updated_task = option[9:]  # Extract updated task name
            # print(len(task_id))
            # print(len(updated_task))
            if task_id == "" or len(task_id) == 0 and len(updated_task) == 0:
                print("Task ID is empty.")
            elif len(task_id) == 0:
                print("No task ID inputed. Please add task ID.")
            else:
                update_task(FILE_NAME, task_id, updated_task)
        elif option.startswith("delete "):
            task_id = option[7:]
            delete_task(FILE_NAME, task_id)
        option = prompt(
        [('class:propmt', 'task-cli '), ('class:input', '')],
        style=style
        )
    print("exit")

def add_task(file_name:str, task_name:str):
    """
    Adds a task to a file based on the users input.
    
    Parameters:
    file_name (str): Name of the file to write data to.
    task_name (str): Name of the task.

    Returns:
    NA
    Displays a status message.
    """
    status = validate_file(file_name)
    data = read_data(file_name)

    # Data processing
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    stripped_task = task_name.strip('"')
    task_status = "todo"

    if len(data) > 0:
        sequential_id = id_generator.generate_task_id(data[len(data) - 1]["id"])
    else:
        # Handle case when data is empty
        sequential_id = id_generator.generate_task_id(0)
    data.append({"id": sequential_id, "task": stripped_task, "createdAt": created_date, "status": task_status})

    if status:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        pass
    print(f"Task added successfully (ID: {str(id_generator)})")

def update_task(file_name:str, task_id:str, updated_task:str):
    """
    Updates a task based on the task ID provided by the user.

    Parameters:
    file_name (string): Represents the file path
    task_id (str): Represents the task ID
    updated_task (str): Represents the updated task that the user inputs

    Returns:
    NA
    Displays a status message.
    """
    status = validate_file(file_name)
    data = read_data(file_name)

    # Data processing
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    task_offset = int(task_id)
    stripped_task = updated_task.strip('"')
    # print(data[2]["id"])
    for task in data:
        if task["id"] == task_offset:
            task.update({"task": stripped_task,"updatedAt": updated_date})

    if status:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    print(f"Task {task_id} updated successfully.")

def delete_task(file_name:str, task_id:str):
    """
    Deletes a task from the tasks.json file based on the ID given.

    Parameters:
    file_name (str): Name of the file to overwrite data.
    task_id (str): Represents the task ID

    Returns:
    NA
    """
    status = validate_file(file_name)
    data = read_data(file_name)

    for i in range(len(data)):
        if data[i]["id"] == int(task_id):
            data.pop(i)
            break

    if status:
        # data[0]["id"] = 
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    
    print(f"Task {task_id} deleted successfully.")

def list_tasks(file_name:str, task_status:str):
    """
    Reads from the file and lists the tasks.
    
    Parameters:
    file_name (str): Name of the file to read/display data from.

    Returns:
    prints a list of tasks and filters them based on status.
    """
    status = validate_file(file_name)
    data = read_data(file_name)

    if status and len(data) != 0:
        if task_status == "":
            for task in data:
                print(f'{task["id"]}: {task["task"]} {task["status"]}')
        elif task_status == "done":
            sort_tasks(data, "done")
        elif task_status == "todo":
            sort_tasks(data, "todo")
        elif task_status == "in-progress":
            sort_tasks(data, "in-progress")
    else:
        print("You haven't added any tasks yet.")

def sort_tasks(tasks:dict, condition:str):
    """
    Sorts the list of tasks depending on the condtion:
    --- todo
    --- in progress
    --- done

    parameters:
    tasks (dict): The dictionary of tasks that will be sorted
    condition (str): The condition to sort by
    """
    sorted_tasks = sorted(tasks, key=lambda item: item["status"] != condition)
    for task in sorted_tasks:
        print(f'{task["id"]}: {task["task"]} {task["status"]}')

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