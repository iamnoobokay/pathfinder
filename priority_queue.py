from queue import PriorityQueue

pq = PriorityQueue()

pq.put((2, "Task 2"))
pq.put((1, 'Task 1'))
pq.put((3, 'Task 3'))


while not pq.empty():
    item = pq.get()
    print(item)

print(pq.empty())
