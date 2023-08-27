import random
import csv

# staff per day
PER = 2
DAYS = 33

# File of staff
FILE = "fullstaff.txt"

staff_array = []
schedule = []

# Column headers for export file
VIL = 'T'
COL_HEADERS = []
for i in range(PER):
    COL_HEADERS.append(VIL + str(i+1))


# open and read the file
try:
    with open(FILE, 'r') as file:
        for line in file:
            staff_array.append(line.strip())
except FileNotFoundError:
    print("File not found.")
except IOError:
    print("An error occurred while reading the file.")
        
# set up
assignments = dict()
for st in staff_array:
        assignments[st] = 0
staff = list(assignments.keys())

# returns lowest value
def lowest(assignments : dict):
    lowest = 100
    for i in list(assignments.values()):
        if i < lowest:
            lowest = i
    return lowest        

# Check for past assignment
def check(staff):
    assign = schedule[-1]
    for x in range(PER):
        if (assign[x] == staff):
            return True
    return False

# assign staff 
def assign():
    on = list()
    while True:
        random.shuffle(staff)
        for st in staff:
            if len(schedule) > 0:
                if check(st):
                    continue
            if (len(on) >= PER):
                schedule.append(on)
                return
            if assignments[st] == lowest(assignments):
                on.append(st)
                assignments[st] += 1
      
# For manually assigning a day

# Needs to be edited to account for changing variables

# def manual(n1,n2,n3,n4):          
#     li = list()
#     li.append(n1)
#     li.append(n2)
#     li.append(n3)
#     li.append(n4)
#     assignments[n1] += 1
#     assignments[n2] += 1
#     assignments[n3] += 1
#     assignments[n4] += 1
#     return li


# printing the schedule
def print_schedule():
    print("-----------------------------------------------------------------------------")
    for a in schedule:
        print(a)
    print("-----------------------------------------------------------------------------")
    print("Number of ODs per each staff:")
    for staff_member in assignments:
        print(staff_member + ": " + str(assignments[staff_member]))
    print("-----------------------------------------------------------------------------")
        
    
    
def export():
    # Path to the CSV file
    csv_file_path = 'od_schedule.csv'

    # Write the data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(COL_HEADERS)
        writer.writerows(schedule)
    
    print("\nData has been exported to " + csv_file_path + '\n')


def main():
    for _ in range(DAYS):
        assign()
    print_schedule()
    export()
    

if __name__ == '__main__':
    main()