def solve(first_machine_exec_time, second_machine_exec_time):
    assert len(first_machine_exec_time) == len(second_machine_exec_time)

    def init(first_machine_exec_time, second_machine_exec_time):
        n_jobs = len(first_machine_exec_time)
        I_set = set()
        J_set = set()
        for i in range(n_jobs):
            if first_machine_exec_time[i] <= second_machine_exec_time[i]:
                I_set.add(i)
            else:
                J_set.add(i)
        a_x = max(first_machine_exec_time[i] for i in I_set)
        x = first_machine_exec_time.index(a_x)
        b_y = max(second_machine_exec_time[j] for j in J_set)
        y = second_machine_exec_time.index(b_y)
        c_max = max(sum(first_machine_exec_time), sum(second_machine_exec_time),
                    max(first_machine_exec_time[i] + second_machine_exec_time[i] for i in range(n_jobs)))
        return I_set, J_set, a_x, x, b_y, y, c_max

    def build_schedule(I_set, J_set, x, c_max, first_machine_exec_time, second_machine_exec_time):
        first_machine = []
        second_machine = []
        cur_time = 0
        for job_idx in I_set - {x, }:
            first_machine.append((job_idx, cur_time, cur_time + first_machine_exec_time[job_idx]))
            cur_time += first_machine_exec_time[job_idx]
        cur_time = c_max - (first_machine_exec_time[x] + sum(first_machine_exec_time[job_idx] for job_idx in J_set))
        for job_idx in J_set:
            first_machine.append((job_idx, cur_time, cur_time + first_machine_exec_time[job_idx]))
            cur_time += first_machine_exec_time[job_idx]
        first_machine.append((x, cur_time, c_max))
        second_machine.append((x, 0, second_machine_exec_time[x]))
        cur_time = second_machine_exec_time[x]
        for job_idx in I_set - {x, }:
            second_machine.append((job_idx, cur_time, cur_time + second_machine_exec_time[job_idx]))
            cur_time += second_machine_exec_time[job_idx]
        cur_time = c_max - sum(second_machine_exec_time[job_idx] for job_idx in J_set)
        for job_idx in J_set:
            second_machine.append((job_idx, cur_time, cur_time + second_machine_exec_time[job_idx]))
            cur_time += second_machine_exec_time[job_idx]
        return first_machine, second_machine

    I_set, J_set, a_x, x, b_y, y, c_max = init(first_machine_exec_time, second_machine_exec_time)
    if a_x > b_y:
        return build_schedule(I_set, J_set, x, c_max, first_machine_exec_time, second_machine_exec_time)
    else:
        I_set, J_set, a_x, x, b_y, y, c_max = init(second_machine_exec_time, first_machine_exec_time)
        first_machine, second_machine = build_schedule(I_set, J_set, x, c_max, second_machine_exec_time,
                                                       first_machine_exec_time)
        return second_machine, first_machine


print(solve([1, 10, 17, 12, 11], [13, 12, 9, 17, 3]))
