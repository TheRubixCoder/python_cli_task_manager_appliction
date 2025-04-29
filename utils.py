import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"epics": [], "subtasks": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

def validate_date(prompt):
    while True:
        date_str = input(prompt + " (YYYY-MM-DD HH:MM): ")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format. Please enter again.")

def validate_positive_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                raise ValueError
            return val
        except ValueError:
            print("Invalid input. Please enter a non-negative number.")

def validate_positive_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def validate_importance():
    while True:
        try:
            importance = int(input("Enter importance (1-5): "))
            if 1 <= importance <= 5:
                return importance
            else:
                raise ValueError
        except ValueError:
            print("Importance must be an integer between 1 and 5.")

def validate_choice():
    while True:
        try:
            importance = int(input("Enter choice (0-7): "))
            if 0 <= importance <= 7:
                return importance
            else:
                raise ValueError
        except ValueError:
            print("Importance must be an integer between 0 and 7.")

def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def calculate_priority(task):
    # Priority = Importance × (Profit / Duration)
    duration = task.get("duration", 1)
    profit = task.get("profit", 0)
    importance = task.get("importance", 1)
    if duration <= 0:
        duration = 1
    return importance * (profit / duration)

def get_next_index(items):
    return max([item.get("index", 0) for item in items], default=0) + 1
