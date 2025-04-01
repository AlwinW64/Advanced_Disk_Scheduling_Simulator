def look(requests, head, direction="right", disk_size=200):
    total_seek_time = 0
    sequence = []
    requests_sorted = sorted(requests)
    
    if direction == "right":
        # Process requests to the right
        right_requests = [r for r in requests_sorted if r >= head]
        for request in right_requests:
            sequence.append(request)
            total_seek_time += abs(head - request)
            head = request
        
        # Process requests to the left (without going to the end)
        left_requests = [r for r in requests_sorted if r < head]
        for request in reversed(left_requests):
            sequence.append(request)
            total_seek_time += abs(head - request)
            head = request
    else:
        # Process requests to the left
        left_requests = [r for r in requests_sorted if r <= head]
        for request in reversed(left_requests):
            sequence.append(request)
            total_seek_time += abs(head - request)
            head = request
        
        # Process requests to the right (without going to the start)
        right_requests = [r for r in requests_sorted if r > head]
        for request in right_requests:
            sequence.append(request)
            total_seek_time += abs(head - request)
            head = request
    
    return sequence, total_seek_time