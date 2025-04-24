class Process:
    def __init__(self, pid, request_sequence):
        self.pid = pid
        self.request_sequence = request_sequence
        self.held_resources = []
        self.current_index = 0
        self.sleep_timer = 0
        self.terminated = False
        self.waiting = False

    def is_done(self):
        return self.terminated

    def is_waiting(self):
        return not self.terminated and self.waiting

    def is_running(self):
        return not self.terminated and not self.waiting and self.sleep_timer == 0

    def tick(self, resources):
        if self.terminated:
            return

        if self.sleep_timer > 0:
            self.sleep_timer -= 1
            self.waiting = False
            return

        if self.current_index >= len(self.request_sequence):
            self.terminated = True
            return

        req = self.request_sequence[self.current_index]

        if isinstance(req, str) and req.startswith("SLEEP_"):
            sleep_time = int(req.split("_")[1])
            self.sleep_timer = sleep_time
            self.current_index += 1
            self.waiting = False
            return

        resource = resources.get(req)
        if resource and resource.request(self.pid):
            self.held_resources.append(req)
            self.current_index += 1
            self.waiting = False
        else:
            self.waiting = True

    def next_request(self):
        if self.current_index >= len(self.request_sequence):
            return None
        return self.request_sequence[self.current_index]

    def release_all(self, resources):
        for res_name in self.held_resources:
            resource = resources.get(res_name)
            if resource:
                resource.release(self.pid)
        self.held_resources.clear()

    def __str__(self):
        state = "Terminated" if self.terminated else ("Waiting" if self.waiting else "Running")
        return f"<Process {self.pid} | State: {state} | Held: {self.held_resources} | Next: {self.next_request()}>"
