from collections import deque

class GameQueue: 
    def __init__(self):
        self.queue = deque()

    def enqueue(self, game):
        self.queue.append(game)

    def deque(self):
        return self.queue.popleft() if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0


