import random
from entities.ticket import Ticket

class SkipNode:
    def __init__(self, ticket, level):
        self.ticket = ticket
        self.forward = [None] * (level + 1)

class SkipList:
    """Слоёный список для билетов"""
    def __init__(self, max_level=4, p=0.5):
        self.max_level = max_level
        self.p = p
        # Заголовочный узел без билета, указывает на начальные элементы уровней
        self.header = self._create_node(self.max_level, None)
        self.level = 0

    def _create_node(self, lvl, ticket):
        return SkipNode(ticket, lvl)

    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, ticket):
        if not isinstance(ticket, Ticket):
            return False

        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].ticket.ticket_id < ticket.ticket_id:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.ticket.ticket_id != ticket.ticket_id:
            rlevel = self._random_level()

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            new_node = self._create_node(rlevel, ticket)

            for i in range(rlevel + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node
            return True
        return False

    def delete(self, ticket_id):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].ticket.ticket_id < ticket_id:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.ticket.ticket_id == ticket_id:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            return True
        return False

    def find(self, ticket_id):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].ticket.ticket_id < ticket_id:
                current = current.forward[i]
        
        current = current.forward[0]
        if current and current.ticket.ticket_id == ticket_id:
            return current.ticket
        return None

    def get_all(self):
        result = []
        current = self.header.forward[0]
        while current:
            result.append(current.ticket)
            current = current.forward[0]
        return result