import sys 
sys.tracebacklimit = 0
import json
import os
import datetime
from tabulate import tabulate

def main():
    file_path = os.path.expanduser("~/track.json")
    check_json_file_exists(file_path)

    command = get_command()

    if not command:
        help_screen()
        sys.exit()

    if is_command_valid(command):
        command = sys.argv[1]
        match (command):
            case "add":
                add_task(file_path)
            case "update":
                update_task(file_path)
            case "delete":
                delete_task(file_path)
            case "mark-done":
                mark_task(file_path, "done")
            case "mark-in-progress":
                mark_task(file_path, "in-progress")
            case "list":
                which_list_function(file_path) 
            case "help":
                help_screen()
    
    else:
        raise ValueError(f"Unknown command '{sys.argv[1]}' for 'track'\n\nType 'track' for help with commands")

  

def add_task(file_path):
    if is_help_needed_command():
        addTaskHelp()
        sys.exit()

    correct_number_args = 3
    assert_correct_args(correct_number_args)
    file_description = sys.argv[2]

    with open(file_path, "r") as file:
        data = json.load(file)

        new_task_dictionary = {}
        # new_task_dictionary is a python dictionary that holds all the new information for the new task
        # This dictionary can be added to the list inside the json file

        is_file_empty = not data["Tasks"]

        if is_file_empty:
            new_task_dictionary["id"] = 1
        else:
            new_task_dictionary["id"] = data["Tasks"][-1]["id"]+1

        new_task_dictionary["description"] = file_description
        new_task_dictionary["status"] = "todo"
        date_added = datetime.datetime.now()
        date_added = f"{date_added.day}/{date_added.month}/{date_added.year} {date_added.strftime("%H")}:{date_added.strftime("%M")}"
        new_task_dictionary["createdAt"] = date_added
        new_task_dictionary["updatedAt"] = date_added
        
        data["Tasks"].append(new_task_dictionary)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    
    new_task_id = new_task_dictionary["id"]
    print(f"Task added successfully (ID: {new_task_id})")

def addTaskHelp():
    print("Add a task")
    print()
    print("Usage:")
    print("  track add FILEDESCRIPTION [flags]")
    print()
    print("Flags:")
    print("  --help     Help for add")
    print()



def update_task(file_path):
    if is_help_needed_command():
        update_task_help()
        sys.exit()
    
    
    correct_number_args = 4
    assert_correct_args(correct_number_args)

    try:
        id = int(sys.argv[2])
    except ValueError:
        raise TypeError("First Argument should be an integer") from None

    data, index = get_task_index(file_path, id)
    # This index refers to the location of our task within the json file


    new_file_description = sys.argv[3]
    
    data["Tasks"][index]["description"] = new_file_description
    data = updatedDate(data, index)


    with open(file_path, "w") as file:
        file.write(json.dumps(data, indent = 2))
        
def update_task_help():
    print("Updates a task")
    print()
    print("Usage:")
    print("  track update ID FILEDESCRIPTION")
    print()
    print("Flags:")
    print("  --help     Help for update")
    print()



def delete_task(file_path):
    if is_help_needed_command():
        delete_task_help()

    else:
        
        assert len(sys.argv) == 3, f"Requires 1 args, received {len(sys.argv)-2}"
        try:
            id = int(sys.argv[2])
        except ValueError:
            raise ValueError("The argument should be an integer") from None

        
        assert_file_not_empty(file_path)
        
        data, index = get_task_index(file_path, id)

        data["Tasks"].pop(index)
        
        with open(file_path, "w") as file:
            file.write(json.dumps(data, indent=2))        

def delete_task_help():
    print("Delete a task")
    print()
    print("Usage:")
    print("  track delete ID [flags]")
    print()
    print("Flags:")
    print("  --help     Help for delete")
    print()


def mark_task(file_path, new_status):
    if is_help_needed_command():
        if sys.argv[1] == "mark-in-progress":
            mark_in_progress_help()
        elif sys.argv[1] == "mark-done":
            mark_done_help()
        sys.exit()

    correct_number_args = 3    
    assert_correct_args(correct_number_args)
    
    try:
        id = int(sys.argv[2])
    except ValueError:
        raise ValueError("ID should be an integer") from None

    
    data, index = get_task_index(file_path, id)

    data["Tasks"][index]["status"] = new_status
    data = updatedDate(data, index)

    with open(file_path, "w") as file:
        file.write(json.dumps(data, indent = 2))


def mark_in_progress_help():
    print(" Mark a task as in progress")
    print()
    print("Usage:")
    print("  track mark-in-progress ID")
    print()
    print("Flags:")
    print("  --help     Help for update")
    print()



def mark_done_help():
    print(" Mark a task as completed")
    print()
    print("Usage:")
    print("  track mark-done ID")
    print()
    print("Flags:")
    print("  --help     Help for update")
    print()


def list_specific_tasks(file_path, status):
    if is_help_needed_command():
        list_all_tasks_help()
    
    else:
        correct_number_args = 3
        assert_correct_args(correct_number_args)


        print(f"{status.title()} Tasks:")
        with open(file_path, "r") as file:
            data = json.load(file)
            number_of_tasks = len(data["Tasks"])
            table = []
            for i in range(number_of_tasks):
                if data["Tasks"][i]["status"] == status:
                    table.append([data["Tasks"][i][header] for header in data["Tasks"][i].keys()])
        
        print(tabulate(table, headers = ["ID", "Description", "Status ", "Date OF Creation", "Last Updated"]))


        print()

def list_all_tasks(file_path):
    correct_number_args = 2
    assert_correct_args(correct_number_args)
    
    print("All tasks:")

    with open(file_path, "r") as file:
        data = json.load(file)
        tasks = data["Tasks"]
        table = []
        for task in tasks:
            table.append([task[header] for header in task.keys()])
        
    print(tabulate(table, headers = ["ID", "Description", "Status ", "Date OF Creation", "Last Updated"]))

    print()

def list_all_tasks_help():
    print("List tasks")
    print()
    print("Usage:")
    print("  track list [flags]")
    print()
    print("Flags:")
    print("  todo             List all incomplete tasks")
    print("  done             List all completed tasks")
    print("  in-progress      List all tasks that are in progress")
    print("  --help           Help for list")
    print()



def create_json_file(file_path):
    with open(file_path, "w") as data:
        empty_tasks_dict = {
            "Tasks": []
        }
        json.dump(empty_tasks_dict, data)

def check_json_file_exists(file_path):
    json_file_exists = os.path.exists(file_path)

    if not json_file_exists:
        create_json_file(file_path)

def get_command():
    if len(sys.argv) == 1:
        return None

    else:
        return sys.argv[1]

def is_command_valid(command):   
    listOfCommands = ["add", "update", "delete", "list", "help", "mark-done", "mark-in-progress"]
    return command in listOfCommands


def is_help_needed_command():
    return len(sys.argv) == 3 and sys.argv[2]=="--help"  

def assert_correct_args(correct_number_args):
    assert len(sys.argv) == correct_number_args, f"Requires {correct_number_args-2} args, received {len(sys.argv)-2}"


def get_task_index(file_path, id):
    is_valid_id = False

    with open(file_path, "r") as file:
        data = json.load(file)
        for i in range(len(data["Tasks"])):
            if data["Tasks"][i]["id"] == id:
                index = i
                is_valid_id = True
    assert is_valid_id, "Invalid ID"
    return data, index

def assert_file_not_empty(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        assert data["Tasks"], "No tasks are in the list" 

'''def checkTheCommand():
    
    if len(sys.argv) == 1:
        help_screen()

    else:
        command = sys.argv[1]
        
        listOfCommands = ["add", "update", "delete", "list", "help", "mark-done", "mark-in-progress"]
        assert command in listOfCommands, f"Unknown command '{sys.argv[1]}' for 'track'\n\nType 'track' for help with commands"

        match (command):
            case "add":
                addTask()
            case "update":
                updateTask()
            case "delete":
                deleteTask()
            case "mark-done":
                mark_task("done")
            case "mark-in-progress":
                mark_task("in-progress")
            case "list":
                which_list_function() 
            case "help":
                help_screen()'''

def which_list_function(file_path):
    if len(sys.argv) == 2:
        list_all_tasks(file_path)
        sys.exit()

    list_of_args = ["--help", "done", "todo", "in-progress"]
    argument = sys.argv[2]
    assert argument in list_of_args, f"Unknown args '{sys.argv[2]}' for 'track list'"

    match (argument):
        case "--help":
            list_all_tasks_help(file_path)
        case "done":
            list_specific_tasks(file_path, "done")
        case "todo":
            list_specific_tasks(file_path, "todo")
        case "in-progress":
            list_specific_tasks(file_path, "in-progress")


def updatedDate(data, index):

    date_updated = datetime.datetime.now()
    date_updated = f"{date_updated.day}/{date_updated.month}/{date_updated.year} {date_updated.strftime("%H")}:{date_updated.strftime("%M")}"
    data["Tasks"][index]["updatedAt"] = date_updated
    return data


def help_screen():
    print("Usage:")
    print("  track [command]")
    print()
    print("Available Commands:")
    print("  add                Add a new task")
    print("  update             Update a task")
    print("  delete             Delete a task")
    print("  mark-in-progress   Mark a task as in progress")
    print("  mark-done          Mark a task as complete")
    print("  list               List all tasks")
    print("  list done          List all completed tasks")
    print("  list todo          List all incomplete tasks")
    print("  list in-progress   List all tasks that are in progress")
    print("  help               Help with any command")
    print()
    print("Use 'track [command] --help' for more information about a command.")
    print()
            
if __name__ == "__main__":
    main()