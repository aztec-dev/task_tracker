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
    """
    Adds a task to tasks.json based on user input
    
    Parameters:
    file_name (str): Name of the file to write data to.
    json_object (dict): Python dict that is written into the file.

    Returns:
    NA
    prints a status message.
    """
    status = validate_file(file_name)
    data = read_data(file_name)
    if status == True:
        json_object["id"] += 1
        data.update(json_object)
        with open(file_name, 'a+') as outfile:
            outfile.seek(0, 2)
            file_position = outfile.tell()

            if file_position == 0:
                outfile.write('[\n')
            else:
                outfile.seek(file_position - 1, 0)
                last_char = outfile.read(1)

                if last_char != ']':
                    outfile.seek(file_position - 1, 0)
                    outfile.write(',\n')
            json.dump(data, outfile)
            outfile.write('\n]')
    print(f"Task added successfully (ID: {json_object["id"]})")

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
    if status == True and len(data) != 0:
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
        create_file(file_name)
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
    if status == True:
        if os.stat(file_name).st_size == 0:
            return {}  # Return an empty dictionary if the file is empty
        else:
            with open(file_name, 'r') as outfile:
                data = json.load(outfile)
    return data

def create_file(file_name:str):
    """
    Creates a new file containing an empty array.

    Parameters:
    file_name (str): Name of the file to be validated.

    Returns:
    list: An empty list that is written into the new file.
    """
    with open(file_name, 'x'):
        pass
    pass
main()