def scan(requests, head, direction="right", disk_size=200):
    total_seek_time = 0
    sequence = []
    requests_sorted = sorted(requests)

    if direction == "right":
        right = [r for r in requests_sorted if r >= head]
        left = [r for r in requests_sorted if r < head]

        for r in right:
            total_seek_time += abs(head - r)
            sequence.append(r)
            head = r

        if head != disk_size - 1:
            total_seek_time += abs(head - (disk_size - 1))
            sequence.append(disk_size - 1)
            head = disk_size - 1

        for r in reversed(left):
            total_seek_time += abs(head - r)
            sequence.append(r)
            head = r

    else:
        left = [r for r in requests_sorted if r <= head]
        right = [r for r in requests_sorted if r > head]

        for r in reversed(left):
            total_seek_time += abs(head - r)
            sequence.append(r)
            head = r

        if head != 0:
            total_seek_time += abs(head - 0)
            sequence.append(0)
            head = 0

        for r in right:
            total_seek_time += abs(head - r)
            sequence.append(r)
            head = r

    return sequence, total_seek_time
