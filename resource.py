class Resource:
    def __init__(self, name, total):
        self.name = name
        self.total = total          # ✅ Needed by visualizer
        self.available = total
        self.held_by = {}           # {pid: count}

    def request(self, pid, amount=1):
        if self.available >= amount:
            self.available -= amount
            self.held_by[pid] = self.held_by.get(pid, 0) + amount
            return True
        return False

    def release(self, pid):
        if pid in self.held_by:
            released = self.held_by.pop(pid)
            self.available += released

    def release_all(self, pid):
        """Alias for release(pid) – included for clarity and compatibility."""
        self.release(pid)
