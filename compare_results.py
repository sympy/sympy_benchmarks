import json
import sys
def load_results(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception:
        print(f"Error reading file: {path}")
        sys.exit(1)
    return data.get("results", {})
def extract_times(results):
    times = {}
    for name, info in results.items():
        if not isinstance(info, dict):
            continue
        result = info.get("result")
        if result is None:
            continue
        if isinstance(result, list):
            for i, val in enumerate(result):
                if isinstance(val, (int, float)):
                    times[f"{name}[{i}]"] = val
        elif isinstance(result, (int, float)):
            times[name] = result
    return times
def compare(old_file, new_file, threshold=10.0):
    old_times = extract_times(load_results(old_file))
    new_times = extract_times(load_results(new_file))
    print(f"\nComparing results (threshold={threshold}%)\n")
    reg_found = False
    for name in sorted(set(old_times) | set(new_times)):
        old = old_times.get(name)
        new = new_times.get(name)
        if old is None:
            print(f"NEW: {name}")
            continue
        if new is None:
            print(f"REMOVED: {name}")
            continue
        if old == 0:
            continue
        change = ((new - old) / old) * 100
        if change > threshold:
            print(f"REGRESSION: {name} {change:+.2f}%")
            reg_found = True
        elif change < -threshold:
            print(f"IMPROVEMENT: {name} {change:+.2f}%")
        else:
            print(f"OK: {name} {change:+.2f}%")
    if reg_found:
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_results.py old.json new.json [threshold]")
        sys.exit(1)
    thresh = 10.0
    if len(sys.argv) == 4:
        thresh = float(sys.argv[3])
    compare(sys.argv[1], sys.argv[2], thresh)