
def clook(requests, head, direction="right", disk_size=200):
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

        if left:
            total_seek_time += abs(head - left[0])
            head = left[0]

        for r in left:
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

        if right:
            total_seek_time += abs(head - right[-1])
            head = right[-1]

        for r in reversed(right):
            sequence.append(r)
            total_seek_time += abs(head - r)
            head = r

    return sequence, total_seek_time