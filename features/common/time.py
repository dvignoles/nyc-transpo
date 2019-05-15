from datetime import time

times = []
for i in range(0, 24):
    times.append(time(i, 0, 0))
    times.append(time(i, 30, 0))

def time_to_val(t):
    for index, time in enumerate(times):
        if (t < time):
            return (index - 1)
    return 47
