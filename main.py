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
\033[33mupdate [ID] [task name/description]\033[0m => updates a task based on ID\n\
\033[33mdelete [ID]\033[0m => deletes a task based on ID\n\
\033[33mmark-[condition]\033[0m => mark a task as done, todo, in-progress\n\
\033[33mlist [status]\033[0m => list all tasks based on status\n"


def main():
    """
    Behold, the program!
    """
    print(MENU)
    status = validate_file(FILE_NAME)
    data = read_data(FILE_NAME)
    # option = input('task-cli ')
    option = prompt(
        [('class:propmt', 'task-cli '), ('class:input', '')],
        style=style,
    )

    while option != "exit":
        if option.startswith("list"):
            condition = option[5:]  # Extract condition
            list_tasks(condition, status, data)
        elif option.startswith("add "):
            task_name = option[4:]  # Extract task name
            add_task(FILE_NAME, task_name, status, data)
        elif option.startswith("update"):
            task_id = option[7:8]  # Extract task ID
            updated_task = option[9:]  # Extract updated task name
            if task_id == "":  # Handle empty ID case.
                print("\033[1;31;48mNo valid task ID defined. Try again.\033[0")
            elif task_id == "0":  # Handle 0 index ID case.
                print("\033[1;31;48mID can't be 0. Try again.\033[0")
            elif len(updated_task) == 0:  # Handle empty task name/description case
                print("\033[1;31;48mNo new task name/description defined. Try again.\033[0m")
            else:
                update_task(FILE_NAME, task_id, updated_task, status, data)
        elif option.startswith("delete"):
            task_id = option[7:]
            delete_task(FILE_NAME, task_id, status, data)
        elif option.startswith("mark-"):
            condition = option[5:]
            mark_task(condition)
        else:
            print("\033[1;31;48mIncorrect command. Try again.\033")
        option = prompt(
        [('class:propmt', 'task-cli '), ('class:input', '')],
        style=style
        )
    print("exit")

def add_task(file_name:str, task_name:str, status:bool, data:list):
    """
    Adds a task to a file based on the users input.
    
    Parameters:
    file_name (str): Name of the file to write data to.
    task_name (str): Name of the task.
    status (bool): Bool value defining the state of the file.
    data (list): Represents a list of dictionary objects that represents a task.

    Returns:
    Displays a status message.
    """

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
    print(f"Task added successfully (ID: {str(id_generator)})")

def update_task(file_name:str, task_id:str, updated_task:str, status:bool, data:list):
    """
    Updates a task based on the task ID provided by the user.

    Parameters:
    file_name (string): Represents the file path
    task_id (str): Represents the task ID
    updated_task (str): Represents the updated task that the user inputs
    status (bool): Bool value defining the state of the file.
    data (list): Represents a list of dictionary objects that represents a task.

    Returns:
    Displays a status complete message.
    """

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

def delete_task(file_name:str, task_id:str, status:bool, data:list):
    """
    Deletes a task from the tasks.json file based on the ID given.

    Parameters:
    file_name (str): Name of the file to overwrite data.
    task_id (str): Represents the task ID
    status (bool): Bool value defining the state of the file.
    data (list): Represents a list of dictionary objects that represents a task.

    Returns:
    Displays a status complete message.
    """

    for i in range(len(data)):
        if data[i]["id"] == int(task_id):
            data.pop(i)
            break

    if status:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    
    print(f"Task {task_id} deleted successfully.")

def list_tasks(task_status:str, status:bool, data:list):
    """
    Reads from the file and lists the tasks.
    
    Parameters:
    file_name (str): Name of the file to read/display data from.
    status (bool): Bool value defining the state of the file.
    data (list): Represents a list of dictionary objects that represents a task.

    Returns:
    Displays a list of tasks and filters them based on status.
    """

    if status and len(data) != 0:
        if task_status == "":
            for task in data:
                print(f'{task["id"]}: {task["task"]} {task["status"]}')
        elif task_status == "done":
            list_condition(data, "done")
        elif task_status == "todo":
            list_condition(data, "todo")
        elif task_status == "in-progress":
            list_condition(data, "in-progress")
    else:
        print("You haven't added any tasks yet.")

def list_condition(tasks:list, condition:str):
    """
    List the tasks depending on the condtion:
    --- todo
    --- in progress
    --- done

    parameters:
    tasks (dict): The dictionary of tasks that will be sorted
    condition (str): The condition to sort by

    Returns:
    list: List of tasks based on condition specified.
    """
    required_tasks = [task for task in tasks if task["status"] == condition]
    for x in range(len(required_tasks)):
        print(f"{required_tasks[x]["id"]}: {required_tasks[x]["task"]} {required_tasks[x]["status"]}")
    

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

def mark_task(file_name:str, condition:str):
    """
    Marks a task as in-progress or done.

    Paramteres:
    file_name (str): Name of the file containing 
    """
    
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