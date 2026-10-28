from time import monotonic
import heapq

def send_all(requests, send_batch) -> None:
    queue = []
    num = 0

    while num < len(requests):
        heapq.heappush(queue, (monotonic(), requests[num]))
        num += 1
    
    while queue:
        batch = []
        while queue and queue[0][0] <= monotonic() and len(batch) < 5:
            request = heapq.heappop(queue)
            batch.append(request[1])

        if batch:
            response = send_batch(batch)

            for result in response:
                if result["success"] == False:
                    heapq.heappush(queue, (monotonic() + result["time_delay"], result["request"]))

        