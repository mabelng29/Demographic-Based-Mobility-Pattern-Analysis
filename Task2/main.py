"""
COMP20008 Elements of Data Processing
2025 Semester 2
Assignment 1

Solution: main file

DO NOT CHANGE THIS FILE!
"""

import os
import sys


def verify_task2_1():
    try:
        from task2_1 import task2_1
    except ImportError:
        print("Task 2.1's function not found.")
        return

    print("=" * 80)
    print("Executing Task 2.1...\n")
    task2_1()

    print("Checking Task 2.1's output...\n")
    for expected_file in ["task2_1.png"]:
        if os.path.isfile(expected_file):
            print(f"\tTask 2.1's {expected_file} output found.\n")
            if os.path.getsize(expected_file) == 0:
                print(f"\t❗ Task 2.1's {expected_file} output has size zero - please verify it uploaded correctly.\n")
        else:
            print(f"\t❗ Task 2.1's {expected_file} output NOT found. Please check your code.\n")

    print("Finished Task 2.1")
    print("=" * 80)


def verify_task2_2():

    try:
        from task2_2 import task2_2
    except ImportError:
        print("Task 2.2's function not found.")
        return

    print("=" * 80)
    print("Executing Task 2.2...\n")
    task2_2()

    print("Checking Task 2.2's output...\n")
    for expected_file in ["task2_2.png"]:
        if os.path.isfile(expected_file):
            print(f"\tTask 2.2's {expected_file} output found.\n")
            if os.path.getsize(expected_file) == 0:
                print(f"\t❗ Task 2.2's {expected_file} output has size zero - please verify it uploaded correctly.\n")
        else:
            print(f"\t❗ Task 2.2's {expected_file} output NOT found. Please check your code.\n")

    print("Finished Task 2.2")
    print("=" * 80)


def main():
    args = sys.argv
    assert len(args) >= 2, "Please provide a task."
    task = args[1]
    valid_tasks = ["all"] + ["task2_" + str(i) for i in range(1, 3)]
    assert task in valid_tasks, \
        f"Invalid task \"{task}\", options are: {valid_tasks}."
    if task == "task2_1":
        verify_task2_1()
    elif task == "task2_2":
        verify_task2_2()
    elif task == "all":
        verify_task2_1()
        verify_task2_2()

if __name__ == "__main__":
    main()

