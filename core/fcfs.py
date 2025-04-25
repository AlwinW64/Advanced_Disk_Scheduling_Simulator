def fcfs(requests, head):
    total_seek_time = 0
    sequence = []
    for request in requests:
        seek_time = abs(head - request)
        total_seek_time += seek_time
        sequence.append(request)
        head = request
    return sequence, total_seek_time