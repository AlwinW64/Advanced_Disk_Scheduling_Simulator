def cscan(requests, head, direction="right", disk_size=200):
    total_seek_time = 0
    sequence = []
    requests_sorted = sorted(requests)
    if direction == "right":
        for i in range(head, disk_size):
            if i in requests_sorted:
                sequence.append(i)
                total_seek_time += abs(head - i)
                head = i
                requests_sorted.remove(i)
        sequence.append(disk_size - 1)
        total_seek_time += abs(head - (disk_size - 1))
        head = 0
        for i in range(0, disk_size):
            if i in requests_sorted:
                sequence.append(i)
                total_seek_time += abs(head - i)
                head = i
                requests_sorted.remove(i)
    else:
        for i in range(head, -1, -1):
            if i in requests_sorted:
                sequence.append(i)
                total_seek_time += abs(head - i)
                head = i
                requests_sorted.remove(i)
        sequence.append(0)
        total_seek_time += abs(head - 0)
        head = disk_size - 1
        for i in range(disk_size - 1, -1, -1):
            if i in requests_sorted:
                sequence.append(i)
                total_seek_time += abs(head - i)
                head = i
                requests_sorted.remove(i)
    return sequence, total_seek_time
