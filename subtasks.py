import json
from datetime import datetime, timedelta
from utils import load_data, save_data, validate_date, validate_positive_float, validate_positive_int, validate_importance, merge_sort, calculate_priority

def create_subtask():
    data = load_data()
    if not data['epics']:
        print("No epics found. Create an epic first.")
        return

    for idx, epic in enumerate(data['epics']):
        print(f"{idx}: {epic['title']}")
    try:
        epic_index = int(input("Select the index of the epic to add a subtask to: "))
        if epic_index < 0 or epic_index >= len(data['epics']):
            raise ValueError
    except ValueError:
        print("Invalid index.")
        return

    epic = data['epics'][epic_index]
    # Remove auto-subtask if this is the first custom subtask
    data['subtasks'] = [s for s in data['subtasks'] if not (s['epic_index'] == epic_index and s['title'] == epic['title'])]

    title = input("Enter subtask title: ")
    description = input("Enter description: ")
    duration = validate_positive_float("Enter duration (in days): ")
    profit = validate_positive_float("Enter profit (0 if none): ")
    importance = validate_importance()

    priority = importance * (profit / duration if duration > 0 else 0)
    subtask = {
        "index": len(data['subtasks']),
        "epic_index": epic_index,
        "title": title,
        "description": description,
        "duration": duration,
        "profit": profit,
        "importance": importance,
        "priority": priority,
        "deadline": epic['deadline']  # Inherit from parent epic
    }
    data['subtasks'].append(subtask)
    save_data(data)
    print("Subtask added successfully.")

def show_subtasks_under_epic():
    data = load_data()
    if not data['epics']:
        print("No epics available.")
        return

    for idx, epic in enumerate(data['epics']):
        print(f"{idx}: {epic['title']}")
    try:
        epic_index = int(input("Select the index of the epic: "))
        if epic_index < 0 or epic_index >= len(data['epics']):
            raise ValueError
    except ValueError:
        print("Invalid index.")
        return

    subtasks = [s for s in data['subtasks'] if s['epic_index'] == epic_index]
    subtasks = merge_sort(subtasks, 'priority')
    if not subtasks:
        print("No subtasks available for this epic.")
        return

    for sub in subtasks:
        print(f"{sub['title']} | Priority: {sub['priority']:.2f} | Deadline: {sub['deadline']} | Duration: {sub['duration']} days")

def delete_subtask():
    data = load_data()
    if not data['subtasks']:
        print("No subtasks to delete.")
        return

    for idx, sub in enumerate(data['subtasks']):
        print(f"{idx}: {sub['title']} (Epic: {data['epics'][sub['epic_index']]['title']})")
    try:
        del_index = int(input("Enter index of subtask to delete: "))
        if del_index < 0 or del_index >= len(data['subtasks']):
            raise ValueError
    except ValueError:
        print("Invalid index.")
        return

    del data['subtasks'][del_index]
    # Reassign indices
    for i, sub in enumerate(data['subtasks']):
        sub['index'] = i
    save_data(data)
    print("Subtask deleted successfully.")

def weighted_job_scheduling(subtasks):
    # Sort jobs by deadline (end time)
    subtasks = merge_sort(subtasks, key=lambda x: x['deadline'])

    # Convert deadlines and durations into start and end times
    for task in subtasks:
        task['start'] = (datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M") - timedelta(days=task['duration'])).strftime("%Y-%m-%d %H:%M")

    # Sort by end time again
    subtasks = merge_sort(subtasks, key=lambda x: x['deadline'])

    # Precompute the latest non-conflicting job index
    def binary_search_latest_non_conflicting(i):
        low, high = 0, i - 1
        while low <= high:
            mid = (low + high) // 2
            if subtasks[mid]['deadline'] <= subtasks[i]['start']:
                if mid + 1 < len(subtasks) and subtasks[mid + 1]['deadline'] <= subtasks[i]['start']:
                    low = mid + 1
                else:
                    return mid
            else:
                high = mid - 1
        return -1

    n = len(subtasks)
    dp = [0] * n
    selected = [None] * n

    for i in range(n):
        incl_prof = subtasks[i]['priority']
        l = binary_search_latest_non_conflicting(i)
        if l != -1:
            incl_prof += dp[l]

        if incl_prof > (dp[i - 1] if i > 0 else 0):
            dp[i] = incl_prof
            selected[i] = l
        else:
            dp[i] = dp[i - 1] if i > 0 else 0
            selected[i] = selected[i - 1] if i > 0 else None

    # Reconstruct the optimal job subset
    def find_selected_jobs(i):
        result = []
        while i >= 0:
            l = binary_search_latest_non_conflicting(i)
            if dp[i] == (dp[l] + subtasks[i]['priority'] if l != -1 else subtasks[i]['priority']):
                result.append(subtasks[i])
                i = l
            else:
                i -= 1
        return list(reversed(result))

    result = find_selected_jobs(n - 1)
    print("\n--- Optimized Subtask Schedule (Weighted Job Scheduling) ---")
    for task in result:
        print(f"Epic: {task['epic_index']}, Title: {task['title']}, Priority: {task['priority']:.2f}, Deadline: {task['deadline']}, Duration: {task['duration']} days")


def display_all_subtasks():
    data = load_data()
    subtasks = []

    for task in data['subtasks']:
        # Recalculate priority to ensure up-to-date
        task['priority'] = calculate_priority(task)
        subtasks.append(task)

    if not subtasks:
        print("\nNo subtasks found.")
        return

    weighted_job_scheduling(subtasks)

