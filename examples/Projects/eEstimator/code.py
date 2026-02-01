import random

def estimate_e(trials:int=1000):
    total_count = 0

    for _ in range(trials):
        sum_ = 0
        count = 0
        while sum_ < 1:
            sum_ += random.random()
            count += 1
        total_count += count

    return total_count / trials

if __name__ == "__main__":
    trials = 10000
    e_estimate = estimate_e(trials)
    print(f"Estimated e after {trials} trials: {e_estimate}")
