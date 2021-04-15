def solve(first_machine_exec_time, second_machine_exec_time):
    assert len(first_machine_exec_time) == len(second_machine_exec_time)
    n_jobes = len(first_machine_exec_time)
    not_assigned_jobes = set(range(n_jobes))
    l = []
    r = []
    while not_assigned_jobes:
        min_pij = None
        min_job_idx = None
        min_pij_machine_idx = None
        for job_idx in not_assigned_jobes:
            if min_pij is None or first_machine_exec_time[job_idx] < min_pij:
                min_pij = first_machine_exec_time[job_idx]
                min_job_idx = job_idx
                min_pij_machine_idx = 0
            if second_machine_exec_time[job_idx] < min_pij:
                min_pij = second_machine_exec_time[job_idx]
                min_job_idx = job_idx
                min_pij_machine_idx = 1
        if min_pij_machine_idx == 0:
            l.append(min_job_idx)
        else:
            r.append(min_job_idx)
        not_assigned_jobes.remove(min_job_idx)
    first_machine_jobs = []
    second_machine_jobs = []
    for job_idx in l + r:
        first_machine_start_time = first_machine_jobs[-1][2] if len(first_machine_jobs) > 0 else 0
        first_machine_end_time = first_machine_start_time + first_machine_exec_time[job_idx]
        first_machine_jobs.append((job_idx, first_machine_start_time, first_machine_end_time))
        second_machine_start_time = max(first_machine_end_time, second_machine_jobs[-1][2] if len(
            second_machine_jobs) > 0 else first_machine_end_time)
        second_machine_end_time = second_machine_start_time + second_machine_exec_time[job_idx]
        second_machine_jobs.append((job_idx, second_machine_start_time, second_machine_end_time))
    return first_machine_jobs, second_machine_jobs


print(solve([1, 10, 17, 12, 11], [13, 12, 9, 17, 3]))
