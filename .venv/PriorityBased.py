#user input
n = int(input("Enter number of processes: "))

original_processes = []
for i in range(n):
    print(f"\nProcess P{i+1}")
    at = int(input("Arrival Time: "))
    bt = int(input("Burst Time: "))
    pr = int(input("Priority (lower number = higher priority): "))
    original_processes.append({
        "name": f"P{i+1}",
        "AT": at,
        "BT": bt,
        "priority": pr
    })


# non preempt
def priority_nonpreemptive(proc_list):
    processes = sorted([p.copy() for p in proc_list], key=lambda x: x["AT"])
    time = 0
    completed = []
    waiting_time = {}
    turnaround_time = {}
    ready = []

    while processes or ready:
        ready += [p for p in processes if p["AT"] <= time]
        processes = [p for p in processes if p["AT"] > time]

        if ready:
            ready.sort(key=lambda x: x["priority"])
            current = ready.pop(0)

            start_time = time
            time += current["BT"]
            end_time = time

            tat = end_time - current["AT"]
            wt = tat - current["BT"]

            waiting_time[current["name"]] = wt
            turnaround_time[current["name"]] = tat

            completed.append({
                "name": current["name"],
                "AT": current["AT"],
                "BT": current["BT"],
                "priority": current["priority"],
                "start": start_time,
                "end": end_time
            })
        else:
            time += 1  # cpu idlee

    return completed, waiting_time, turnaround_time


#preempt
def priority_preemptive(proc_list):
    processes = sorted([p.copy() for p in proc_list], key=lambda x: x["AT"])

    for p in processes:
        p["remaining"] = p["BT"]

    time = 0
    completed = []
    waiting_time = {}
    turnaround_time = {}
    ready = []
    current = None
    gantt = []

    while processes or ready or current:
        ready += [p for p in processes if p["AT"] <= time]
        processes = [p for p in processes if p["AT"] > time]


        if current:
            ready.append(current)
            current = None

        if ready:
            ready.sort(key=lambda x: x["priority"])
            current = ready.pop(0)


            gantt.append((time, current["name"]))
            current["remaining"] -= 1
            time += 1


            if current["remaining"] == 0:
                end_time = time
                tat = end_time - current["AT"]
                wt = tat - current["BT"]
                waiting_time[current["name"]] = wt
                turnaround_time[current["name"]] = tat
                completed.append({
                    "name": current["name"],
                    "AT": current["AT"],
                    "BT": current["BT"],
                    "priority": current["priority"],
                    "start": current["AT"],
                    "end": end_time
                })
                current = None

        else:
            time += 1  #cpu idle
    gantt_blocks = []
    if gantt:
        last_name = gantt[0][1]
        start = gantt[0][0]
        for i in range(1, len(gantt)):
            if gantt[i][1] != last_name:
                gantt_blocks.append((last_name, start, gantt[i][0]))
                last_name = gantt[i][1]
                start = gantt[i][0]
        gantt_blocks.append((last_name, start, time))

    return completed, waiting_time, turnaround_time, gantt_blocks


#execute bot h algo
non_completed, non_wt, non_tat = priority_nonpreemptive(original_processes)
pre_completed, pre_wt, pre_tat, gantt_blocks = priority_preemptive(original_processes)

#non preempt results
print("\n=== NON-PREEMPTIVE PRIORITY SCHEDULING ===")
print("Gantt Chart:")
for c in non_completed:
    print(f"| {c['name']} ", end="")
print("|")
print("0", end="")
for c in non_completed:
    print(f"  {c['end']}", end="")
print("\n")

print("Process\tAT\tBT\tPrio\tWT\tTAT")
total_wt = total_tat = 0
for c in non_completed:
    wt = non_wt[c["name"]]
    tat = non_tat[c["name"]]
    total_wt += wt
    total_tat += tat
    print(f"{c['name']}\t{c['AT']}\t{c['BT']}\t{c['priority']}\t{wt}\t{tat}")
print(f"\nAverage WT = {total_wt/n:.2f}")
print(f"Average TAT = {total_tat/n:.2f}")

#preempt results
print("\n=== PREEMPTIVE PRIORITY SCHEDULING ===")
print("Gantt Chart:")
for g in gantt_blocks:
    print(f"| {g[0]} ", end="")
print("|")
print(f"{gantt_blocks[0][1]}", end="")
for g in gantt_blocks:
    print(f"  {g[2]}", end="")
print("\n")

print("Process\tAT\tBT\tPrio\tWT\tTAT")
total_wt = total_tat = 0
for c in pre_completed:
    wt = pre_wt[c["name"]]
    tat = pre_tat[c["name"]]
    total_wt += wt
    total_tat += tat
    print(f"{c['name']}\t{c['AT']}\t{c['BT']}\t{c['priority']}\t{wt}\t{tat}")
print(f"\nAverage WT = {total_wt/n:.2f}")
print(f"Average TAT = {total_tat/n:.2f}")