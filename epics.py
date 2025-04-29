from utils import (
    load_data, validate_date, validate_positive_float,
    validate_positive_int, validate_importance,
    merge_sort, calculate_priority,
    get_next_index, save_data
)
from datetime import datetime

def create_epic():
    data = load_data()
    print("\n--- Create a New Epic ---")
    title = input("Enter title: ")
    description = input("Enter description: ")
    deadline = validate_date("Enter deadline")
    duration = validate_positive_int("Enter duration (in days): ")
    profit = validate_positive_float("Enter profit (can be 0 if none): ")
    importance = validate_importance()

    priority = calculate_priority({
        "duration": duration,
        "profit": profit,
        "importance": importance
    })

    index = len(data["epics"])

    epic = {
        "index": index,
        "title": title,
        "description": description,
        "deadline": deadline.strftime("%Y-%m-%d %H:%M"),
        "duration": duration,
        "profit": profit,
        "importance": importance,
        "priority": priority
    }

    data["epics"].append(epic)

    # If no subtask, consider the epic as a subtask too
    data["subtasks"].append({
        "epic_index": index,
        "title": title,
        "description": description,
        "deadline": deadline.strftime("%Y-%m-%d %H:%M"),
        "duration": duration,
        "profit": profit,
        "importance": importance,
        "priority": priority
    })

    save_data(data)
    print("✅ Epic created successfully!\n")

def delete_epic():
    data = load_data()
    if not data["epics"]:
        print("⚠️  No epics available to delete.\n")
        return

    print("\n--- Delete an Epic ---")
    for i, epic in enumerate(data["epics"]):
        print(f"{i + 1}. {epic['title']} (index: {epic['index']})")

    choice = validate_positive_int("Enter the number of the epic to delete: ")
    if 1 <= choice <= len(data["epics"]):
        epic_to_delete = data["epics"].pop(choice - 1)
        # Remove related subtasks including placeholder epic-as-subtask
        data["subtasks"] = [
            sub for sub in data["subtasks"] if sub.get("index") != epic_to_delete["index"]
        ]
        save_data(data)
        print("✅ Epic deleted successfully.\n")
    else:
        print("❌ Invalid selection.\n")

def show_epics():
    data = load_data()
    if not data["epics"]:
        print("⚠️  No epics to display.\n")
        return

    print("\n--- All Epics (Sorted by Priority using Greedy Method) ---")
    sorted_epics = merge_sort(data["epics"], key=lambda x: x['priority'])[::-1]

    for epic in sorted_epics:
        print(f"\n📌 {epic['title']}")
        print(f"   Index      : {epic['index']}")
        print(f"   Description: {epic['description']}")
        print(f"   Deadline   : {epic['deadline']}")
        print(f"   Duration   : {epic['duration']} days")
        print(f"   Profit     : ₹{epic['profit']}")
        print(f"   Importance : {epic['importance']}")
        print(f"   Priority   : {round(epic['priority'], 2)}")

    print()
