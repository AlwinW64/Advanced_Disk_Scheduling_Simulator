def look(requests, head, direction="right", disk_size=200):
    total_seek_time = 0
    sequence = []
    requests_sorted = sorted(requests)

    if direction == "right":
        right = [r for r in requests_sorted if r >= head]
        left = [r for r in requests_sorted if r < head]

        for r in right:
            sequence.append(r)
            total_seek_time += abs(head - r)
            head = r

        for r in reversed(left):
            sequence.append(r)
            total_seek_time += abs(head - r)
            head = r

    else:
        left = [r for r in requests_sorted if r <= head]
        right = [r for r in requests_sorted if r > head]

        for r in reversed(left):
            sequence.append(r)
            total_seek_time += abs(head - r)
            head = r

        for r in right:
            sequence.append(r)
            total_seek_time += abs(head - r)
            head = r

    return sequence, total_seek_time
