import asyncio

class ObserverServer():
    def __init__(self):
        self.clients = []
        self.ongoing = set()

    def join(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def detach(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def broadcast_event(self, event_id: str, payload = None):
        for task in set(self.ongoing):
            if not task.done():
                self.ongoing.discard(task)

        for client in self.clients:
            task = asyncio.create_task(client.handle_event(event_id, payload))
            self.ongoing.add(task)
            task.start()