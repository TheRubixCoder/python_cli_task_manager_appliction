from epics import create_epic, show_epics, delete_epic
from subtasks import create_subtask, show_subtasks_under_epic, delete_subtask, display_all_subtasks
from utils import load_data, save_data, validate_choice

def main():
    print("Welcome to the Smart Task Manager!\n")

    while True:
        print("\nPlease choose an action:")
        print("1. Create an Epic")
        print("2. Create Subtasks for an Epic")
        print("3. Show All Epics (Greedy - Earliest Deadline First)")
        print("4. Show Subtasks Under a Specific Epic (Sorted by Priority)")
        print("5. Show All Subtasks (Optimized Scheduling - Dynamic Programming)")
        print("6. Delete a Subtask")
        print("7. Delete an Epic")
        print("0. Exit")

        choice = validate_choice()

        if choice == 1:
            create_epic()
        elif choice == 2:
            create_subtask()
        elif choice == 3:
            show_epics()
        elif choice == 4:
            show_subtasks_under_epic()
        elif choice == 5:
            display_all_subtasks()
        elif choice == 6:
            delete_subtask()
        elif choice == 7:
            delete_epic()
        elif choice == 0:
            print("Thanks for using Smart Task Manager. Goodbye!")
            break

if __name__ == "__main__":
    main()
