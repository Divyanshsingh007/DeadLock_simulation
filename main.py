import json
import time
import sys
from process import Process
from resource import Resource
from scheduler import Scheduler
from deadlock_detector import DeadlockDetector
from visualizer import Visualizer

def load_test_case(path):
    with open(path, 'r') as f:
        data = json.load(f)

    resources = {name: Resource(name, total) for name, total in data['resources'].items()}
    processes = [Process(proc['id'], proc['requests']) for proc in data['processes']]
    return processes, resources

def run_simulation(test_case_path):
    print(f"\n=== Deadlock Simulation Starting ===\nTest case: {test_case_path}\n")

    try:
        processes, resources = load_test_case(test_case_path)
    except FileNotFoundError:
        print(f"❌ Could not find test case at: {test_case_path}")
        return

    try:
        scheduler = Scheduler(processes, resources)
        detector = DeadlockDetector()
        visualizer = Visualizer(processes, resources)

        tick = 0
        deadlock_detected = False

        while True:
            visualizer.update(tick)  # Wait for user to click "Next Tick"

            if deadlock_detected or scheduler.all_terminated():
                break

            scheduler.step()
            time.sleep(0.5)

            deadlocked_pids = detector.detect(processes, resources)

            if deadlocked_pids:
                visualizer.mark_deadlock(deadlocked_pids)
                print("\n🚨 Deadlock detected! Involved processes:", deadlocked_pids)
                deadlock_detected = True

            tick += 1

        print("\n✅ Simulation complete.")
        visualizer.run_until_closed()

    except Exception as e:
        print(f"\n❌ An error occurred during simulation: {e}")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "tk":
            import tk_gui
            tk_gui.run_gui()
        else:
            test_case_path = sys.argv[1]
            run_simulation(test_case_path)
    else:
        # Default fallback test case
        run_simulation("test_cases/circular_wait_deadlock_case.json")

if __name__ == "__main__":
    main()
