from pprint import pprint


def sort_with_index(arr):
    arr_with_index = []
    for i, item in enumerate(arr):
        arr_with_index.append((i, item))
    arr_with_index.sort(key=lambda it: -it[1])
    return arr_with_index


def assign(jobs_with_index, n_not_fulfilled_jobs, n_machines):
    assignment = {}
    assigned_jobs = set()
    i = 0
    while i < n_machines and i < n_not_fulfilled_jobs:
        current_job = -1
        for job_idx, job in jobs_with_index:
            if job_idx not in assigned_jobs and job > 0:
                current_job = job_idx
                break
        assigned_jobs.add(current_job)
        assignment[current_job] = i
        i += 1
    return assignment


def level(jobs, machines):
    n_jobs = len(jobs)
    n_machines = len(machines)
    n_not_fulfilled_jobs = len(jobs)
    assignment = []
    t = 0
    while n_not_fulfilled_jobs > 0:
        jobs_with_index = sort_with_index(jobs)
        current_assignment = assign(jobs_with_index, n_not_fulfilled_jobs, n_machines=n_machines)
        dt1 = min(jobs[job_id] / machines[machine_id] for job_id, machine_id in current_assignment.items())
        assignment_list = sorted(current_assignment.items(), key=lambda assg: assg[0])
        dt2 = None
        for start_idx, (job_i, machine_i) in enumerate(assignment_list):
            for job_j, machine_j in assignment_list[start_idx + 1:]:
                if jobs[job_i] <= jobs[job_j] or machines[machine_i] <= machines[machine_j]:
                    continue
                current_dt2 = (jobs[job_i] - jobs[job_j]) / (machines[machine_i] - machines[machine_j])
                if dt2 is None or current_dt2 < dt2:
                    dt2 = current_dt2
        dt = min(dt1, dt2) if dt2 is not None else dt1
        for job_idx in range(n_jobs):
            if jobs[job_idx] > 0:
                if job_idx in current_assignment:
                    machine_idx = current_assignment[job_idx]
                    assignment.append((job_idx, machine_idx, t, t + dt))
                    jobs[job_idx] -= machines[machine_idx] * dt
                    if jobs[job_idx] <= 0:
                        n_not_fulfilled_jobs -= 1
        t += dt
    return assignment


def solve():
    jobs = [7, 8, 4, 9, 12, 5, 3, 9, 5, 12, 7, 5, 8]
    machines = [3, 4, 3, 2]
    return level(jobs, machines)


print(solve())

pprint([(3, 2, 0, 3.0), (4, 0, 0, 3.0), (7, 3, 0, 3.0), (9, 1, 0, 3.0), (0, 2, 3.0, 4.0), (1, 0, 3.0, 4.0),
        (10, 3, 3.0, 4.0), (12, 1, 3.0, 4.0), (1, 0, 4.0, 5.25), (5, 1, 4.0, 5.25), (8, 2, 4.0, 5.25),
        (10, 3, 4.0, 5.25), (0, 1, 5.25, 6.25), (2, 2, 5.25, 6.25), (11, 0, 5.25, 6.25), (12, 3, 5.25, 6.25),
        (4, 0, 6.25, 6.5), (6, 1, 6.25, 6.5), (7, 2, 6.25, 6.5), (10, 3, 6.25, 6.5), (4, 0, 6.5, 6.625),
        (6, 2, 6.5, 6.625), (7, 1, 6.5, 6.625), (10, 3, 6.5, 6.625), (4, 2, 6.625, 6.75), (7, 3, 6.625, 6.75),
        (11, 0, 6.625, 6.75), (12, 1, 6.625, 6.75), (4, 3, 6.75, 7.15625), (6, 1, 6.75, 7.15625),
        (10, 0, 6.75, 7.15625), (11, 2, 6.75, 7.15625), (1, 2, 7.15625, 7.40625), (7, 0, 7.15625, 7.40625),
        (8, 3, 7.15625, 7.40625), (12, 1, 7.15625, 7.40625), (2, 0, 7.40625, 7.59375), (4, 3, 7.40625, 7.59375),
        (7, 1, 7.40625, 7.59375), (8, 2, 7.40625, 7.59375), (1, 1, 7.59375, 7.625), (2, 3, 7.59375, 7.625),
        (10, 0, 7.59375, 7.625), (12, 2, 7.59375, 7.625), (1, 3, 7.625, 7.7265625), (10, 0, 7.625, 7.7265625),
        (11, 1, 7.625, 7.7265625), (12, 2, 7.625, 7.7265625), (1, 3, 7.7265625, 7.7890625),
        (2, 0, 7.7265625, 7.7890625), (4, 1, 7.7265625, 7.7890625), (8, 2, 7.7265625, 7.7890625),
        (2, 0, 7.7890625, 7.8203125), (4, 3, 7.7890625, 7.8203125), (10, 1, 7.7890625, 7.8203125),
        (12, 2, 7.7890625, 7.8203125), (1, 1, 7.8203125, 7.822916666666667), (2, 0, 7.8203125, 7.822916666666667),
        (10, 2, 7.8203125, 7.822916666666667), (12, 3, 7.8203125, 7.822916666666667),
        (1, 1, 7.822916666666667, 7.823784722222222), (2, 0, 7.822916666666667, 7.823784722222222),
        (12, 2, 7.822916666666667, 7.823784722222222), (1, 1, 7.823784722222222, 7.83203125),
        (2, 0, 7.823784722222222, 7.83203125), (2, 0, 7.83203125, 7.8515625), (2, 0, 7.8515625, 7.8515625)])
