class Scheduler:
    def __init__(self, processes, resources):
        self.processes = processes  # List of Process objects
        self.resources = resources  # Dict of Resource objects

    def step(self):
        """Simulate one tick of the system."""
        for process in self.processes:
            if process.is_done():
                continue

            process.tick(self.resources)

            if process.is_done():
                self.release_resources(process.pid)

    def release_resources(self, pid):
        """Release all resources held by a terminated process."""
        for resource in self.resources.values():
            resource.release_all(pid)

    def display_state(self):
        print("\n--- Processes ---")
        for p in self.processes:
            print(p)

        print("\n--- Resources ---")
        for r in self.resources.values():
            print(r)

    def all_terminated(self):
        return all(p.is_done() for p in self.processes)
