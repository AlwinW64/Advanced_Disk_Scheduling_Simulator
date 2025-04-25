def sstf(requests, head):
    total_seek_time = 0
    sequence = []
    requests = requests.copy()
    while requests:
        nearest = min(requests, key=lambda x: abs(x - head))
        seek_time = abs(head - nearest)
        total_seek_time += seek_time
        sequence.append(nearest)
        head = nearest
        requests.remove(nearest)
    return sequence, total_seek_time