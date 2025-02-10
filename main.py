"""
Title: Task Tracker
Date: 10/02/2025
Author: Azariah Pundari (aztec-dev)
"""
import json

tasks = {
    "Id": "1",
    "Task": "sample task",
}

tasks_to_json = json.dumps(tasks, indent=4)

def main():
    """Main program"""
    with open("tasks.json", "a") as task_file:
        # add to file
        task_file.write(tasks_to_json)

main()