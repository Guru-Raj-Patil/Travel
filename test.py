# class Process:
#     def __init__(self, pid, arrival_time, burst_time):
#         self.pid = pid
#         self.arrival_time = arrival_time
#         self.burst_time = burst_time
#         self.remaining_time = burst_time
#         self.completion_time = 0
#         self.turnaround_time = 0
#         self.waiting_time = 0


# def non_preemptive_sjf(processes):
#     processes.sort(key=lambda p: (p.arrival_time, p.burst_time))
#     current_time = 0
#     gantt_chart = []

#     for process in processes:
#         if current_time < process.arrival_time:
#             current_time = process.arrival_time
#         if gantt_chart and gantt_chart[-1][0] == process.pid:
#             gantt_chart[-1] = (
#                 process.pid,
#                 gantt_chart[-1][1],
#                 current_time + process.burst_time,
#             )
#         else:
#             gantt_chart.append(
#                 (process.pid, current_time, current_time + process.burst_time)
#             )
#         current_time += process.burst_time
#         process.completion_time = current_time
#         process.turnaround_time = process.completion_time - process.arrival_time
#         process.waiting_time = process.turnaround_time - process.burst_time

#     return gantt_chart, processes


# def preemptive_sjf(processes):
#     processes.sort(key=lambda p: p.arrival_time)
#     current_time = 0
#     completed = 0
#     n = len(processes)
#     gantt_chart = []
#     ready_queue = []

#     while completed < n:
#         for process in processes:
#             if (
#                 process.arrival_time <= current_time
#                 and process not in ready_queue
#                 and process.remaining_time > 0
#             ):
#                 ready_queue.append(process)

#         ready_queue.sort(key=lambda p: (p.remaining_time, p.arrival_time))

#         if ready_queue:
#             current_process = ready_queue.pop(0)
#             if gantt_chart and gantt_chart[-1][0] == current_process.pid:
#                 gantt_chart[-1] = (
#                     current_process.pid,
#                     gantt_chart[-1][1],
#                     current_time + 1,
#                 )
#             else:
#                 gantt_chart.append(
#                     (current_process.pid, current_time, current_time + 1)
#                 )
#             current_time += 1
#             current_process.remaining_time -= 1

#             if current_process.remaining_time == 0:
#                 current_process.completion_time = current_time
#                 current_process.turnaround_time = (
#                     current_process.completion_time - current_process.arrival_time
#                 )
#                 current_process.waiting_time = (
#                     current_process.turnaround_time - current_process.burst_time
#                 )
#                 completed += 1
#         else:
#             current_time += 1

#     return gantt_chart, processes


# def print_results(title, gantt_chart, processes):
#     print(f"\n{title}")
#     print("\nGantt Chart:")
#     for pid, start_time, end_time in gantt_chart:
#         print(f"| {start_time} P{pid} {end_time} ", end="")
#     print()

#     print("\nProcess Table:")
#     print(
#         "| Process | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time |"
#     )
#     for process in processes:
#         print(
#             f"|   P{process.pid}    |     {process.arrival_time}       |     {process.burst_time}     |        {process.completion_time}       |        {process.turnaround_time}      |      {process.waiting_time}     |"
#         )


# # Input data
# process_list = [
#     Process(1, 0, 10),
#     Process(2, 1, 6),
#     Process(3, 4, 5),
#     Process(4, 5, 8),
#     Process(5, 7, 3),
# ]

# # Non-Preemptive SJF
# np_gantt_chart, np_processes = non_preemptive_sjf(process_list.copy())
# print_results("Non-Preemptive SJF", np_gantt_chart, np_processes)

# # Preemptive SJF
# p_gantt_chart, p_processes = preemptive_sjf(process_list.copy())
# print_results("Preemptive SJF", p_gantt_chart, p_processes)


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def non_preemptive_sjf(processes):
    processes.sort(key=lambda p: (p.arrival_time, p.burst_time))
    current_time = 0
    gantt_chart = []

    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        if gantt_chart and gantt_chart[-1][0] == process.pid:
            gantt_chart[-1] = (
                process.pid,
                gantt_chart[-1][1],
                current_time + process.burst_time,
            )
        else:
            gantt_chart.append(
                (process.pid, current_time, current_time + process.burst_time)
            )
        current_time += process.burst_time
        process.completion_time = current_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

    return gantt_chart, processes


def preemptive_sjf(processes):
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    completed = 0
    n = len(processes)
    gantt_chart = []
    ready_queue = []
    queue_snapshot = []

    while completed < n:
        for process in processes:
            if (
                process.arrival_time <= current_time
                and process not in ready_queue
                and process.remaining_time > 0
            ):
                ready_queue.append(process)

        ready_queue.sort(key=lambda p: (p.remaining_time, p.arrival_time))

        if not queue_snapshot or queue_snapshot[-1][1] != [p.pid for p in ready_queue]:
            queue_snapshot.append((current_time, [p.pid for p in ready_queue]))

        if ready_queue:
            current_process = ready_queue.pop(0)
            if gantt_chart and gantt_chart[-1][0] == current_process.pid:
                gantt_chart[-1] = (
                    current_process.pid,
                    gantt_chart[-1][1],
                    current_time + 1,
                )
            else:
                gantt_chart.append(
                    (current_process.pid, current_time, current_time + 1)
                )
            current_time += 1
            current_process.remaining_time -= 1

            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.turnaround_time = (
                    current_process.completion_time - current_process.arrival_time
                )
                current_process.waiting_time = (
                    current_process.turnaround_time - current_process.burst_time
                )
                completed += 1
        else:
            current_time += 1

    return gantt_chart, processes, queue_snapshot


def print_results(title, gantt_chart, processes, queue_snapshot=None):
    print(f"\n{title}")
    print("\nGantt Chart:")
    for pid, start_time, end_time in gantt_chart:
        print(f"| {start_time} P{pid} {end_time} ", end="")
    print()

    print("\nProcess Table:")
    print(
        "| Process | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time |"
    )
    for process in processes:
        print(
            f"|   P{process.pid}    |     {process.arrival_time}       |     {process.burst_time}     |        {process.completion_time}       |        {process.turnaround_time}      |      {process.waiting_time}     |"
        )

    if queue_snapshot:
        print("\nQueue Snapshot:")
        for time, queue in queue_snapshot:
            print(f"Time {time}: Queue -> {', '.join(f'P{pid}' for pid in queue)}")


# Input data
process_list = [
    Process(1, 0, 10),
    Process(2, 1, 6),
    Process(3, 4, 5),
    Process(4, 5, 8),
    Process(5, 7, 3),
]

# Non-Preemptive SJF
np_gantt_chart, np_processes = non_preemptive_sjf(process_list.copy())
print_results("Non-Preemptive SJF", np_gantt_chart, np_processes)

# Preemptive SJF
p_gantt_chart, p_processes, p_queue_snapshot = preemptive_sjf(process_list.copy())
print_results("Preemptive SJF", p_gantt_chart, p_processes, p_queue_snapshot[::-1])
