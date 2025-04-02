import random
import csv

# File paths
STAFF_FILE = "fullstaff.txt"
SCHEDULE_FILE = "schedule_template.txt"  # Contains O and C entries

# Staff per day
PER = 3
VIL = 'M'

# Read staff list
def load_staff(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print("Staff file not found.")
        exit()
    except IOError:
        print("An error occurred while reading the staff file.")
        exit()

# Read schedule template
def load_schedule_template(file_path):
    try:
        with open(file_path, 'r') as file:
            days = [line.strip() for line in file]
            return days
    except FileNotFoundError:
        print("Schedule file not found.")
        exit()
    except IOError:
        print("An error occurred while reading the schedule file.")
        exit()

# Check if staff was scheduled the previous day
def check_previous_day(schedule, staff):
    if not schedule:
        return False
    return staff in schedule[-1]

# Assign staff evenly across O and C nights
def assign_staff(staff, schedule_template):
    assignments = {st: {'O': 0, 'C': 0} for st in staff}
    schedule = []
    
    def assign_day(day_type):
        available_staff = sorted(
            [s for s in staff if not check_previous_day(schedule, s)],
            key=lambda x: (assignments[x][day_type], sum(assignments[x].values()))
        )
        selected = available_staff[:PER]
        for st in selected:
            assignments[st][day_type] += 1
        return selected
    
    for day in schedule_template:
        schedule.append(assign_day(day))
    
    return schedule, assignments

# Print the schedule
def print_schedule(schedule, assignments):
    print("--------------------------------------------------")
    for day, staff in enumerate(schedule, start=1):
        print(f"Day {day}: {staff}")
    print("--------------------------------------------------")
    print("Assignments per staff:")
    for staff, counts in assignments.items():
        print(f"{staff} -> O: {counts['O']}, C: {counts['C']}, Total: {sum(counts.values())}")
    print("--------------------------------------------------")

# Export schedule to CSV
def export_schedule(schedule):
    csv_file_path = 'od_schedule.csv'
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([VIL + str(i+1) for i in range(PER)])
        writer.writerows(schedule)
    print(f"\nData has been exported to {csv_file_path}\n")

if __name__ == '__main__':
    staff_list = load_staff(STAFF_FILE)
    schedule_template = load_schedule_template(SCHEDULE_FILE)
    schedule, staff_assignments = assign_staff(staff_list, schedule_template)
    print_schedule(schedule, staff_assignments)
    export_schedule(schedule)
