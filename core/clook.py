def clook(requests, head, direction="right", disk_size=200):
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
        
        # Jump to the leftmost request and process remaining left requests
        if requests_sorted and requests_sorted[0] < head:
            total_seek_time += abs(head - requests_sorted[0])
            head = requests_sorted[0]
            left_requests = [r for r in requests_sorted if r < head]
            for request in left_requests:
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
        
        # Jump to the rightmost request and process remaining right requests
        if requests_sorted and requests_sorted[-1] > head:
            total_seek_time += abs(head - requests_sorted[-1])
            head = requests_sorted[-1]
            right_requests = [r for r in requests_sorted if r > head]
            for request in reversed(right_requests):
                sequence.append(request)
                total_seek_time += abs(head - request)
                head = request
    
    return sequence, total_seek_time