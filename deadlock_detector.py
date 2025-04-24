class DeadlockDetector:
    def detect(self, processes, resources):
        """
        Detect cycles in the wait-for graph.
        Return list of process IDs involved in a deadlock (if any).
        """
        wait_for_graph = self.build_wait_for_graph(processes, resources)
        return self.find_cycle(wait_for_graph)

    def build_wait_for_graph(self, processes, resources):
        """
        Returns a dict like:
        {
            "P1": ["P2"],  # P1 is waiting on a resource held by P2
            ...
        }
        """
        graph = {p.pid: [] for p in processes}

        for p in processes:
            if p.is_done():
                continue

            next_res = p.next_request()
            if not next_res:
                continue

            res = resources.get(next_res)
            if res and res.available == 0:
                # Resource unavailable — find who's holding it
                holders = res.held_by.keys()
                graph[p.pid].extend(holders)

        return graph

    def find_cycle(self, graph):
        """
        Detects cycles in the graph using DFS.
        Returns a list of processes involved in deadlock, if any.
        """
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    # Optional: return all nodes in rec_stack
                    return list(rec_stack)

        return []
