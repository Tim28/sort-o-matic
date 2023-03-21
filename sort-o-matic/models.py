import json


class SortOMatic:

    def __init__(self):
        self.inventory = {}

    def add_container(self, container_id):
        self.inventory[container_id] = []

    def add_item(self, container_id, item):
        self.inventory[container_id].append(item)

    def remove_item(self, container_id, item):
        self.inventory[container_id].remove(item)

    def search(self, keyword):
        results = {}
        for container_id in self.inventory:
            for item in self.inventory[container_id]:
                if keyword in item['description']:
                    if container_id not in results:
                        results[container_id] = []
                    results[container_id].append(item)
        return results

    def save_inventory(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.inventory, f)

    def load_inventory(self, filename):
        with open(filename, 'r') as f:
            self.inventory = json.load(f)
