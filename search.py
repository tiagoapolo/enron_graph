class Queue:
    def __init__(self):
        self.items = []
 
    def is_empty(self):
        return self.items == []
 
    def enqueue(self, data):
        self.items.append(data)
 
    def dequeue(self):
        return self.items.pop(0)
 
# Input is type Vertex 
def printBFS(vertex):

    visited = set()
    q = Queue()
    q.enqueue(vertex)
    visited.add(vertex)

    while not q.is_empty():
        current = q.dequeue()
        print(current.get_id(), end=' ')
        for dest in current.get_connections():
            if dest not in visited:
                visited.add(dest)
                q.enqueue(dest)