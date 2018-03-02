import time

def clamp(x, a, b):
    return max(a, min(x, b))

def now():
    return int(round(time.time() * 1000))


def argmax(arr):

    max_val = - float("inf")
    max_id = -1

    for i in range(0, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
            max_id = i

    return max_id

def manhattan_dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)
