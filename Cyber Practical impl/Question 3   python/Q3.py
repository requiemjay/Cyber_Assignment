import hashlib
import time
import random


def mine_block(header, difficulty):
    nonce = 0
    target = "0" * difficulty

    start = time.time()

    while True:
        data = header + str(nonce)
        h = hashlib.sha256(data.encode()).hexdigest()

        if h.startswith(target):
            break

        nonce += 1

    end = time.time()

    return nonce, end - start


difficulty = 2
target_time = 1
total_blocks = 20

times = []
total_nonce = 0

print("PROOF OF WORK SIMULATION")

for i in range(1, total_blocks + 1):

    header = "Block" + str(i)

    nonce, elapsed = mine_block(header, difficulty)

    times.append(elapsed)
    total_nonce += nonce

    print(
        "Block:", i,
        "Nonce:", nonce,
        "Time:", round(elapsed, 4),
        "Difficulty:", difficulty
    )


    if i % 5 == 0:

        avg_time = sum(times) / len(times)

        if avg_time < target_time:
            difficulty += 1

        elif avg_time > target_time:
            difficulty = max(1, difficulty - 1)

        times = []

print("\nTotal Nonces Checked:", total_nonce)


nodes = {
    "Node 1": 50,
    "Node 2": 20,
    "Node 3": 30,
    "Node 4": 40,
    "Node 5": 10
}

random.seed(10)

total_stake = sum(nodes.values())

count = {node: 0 for node in nodes}

print("\nPROOF OF STAKE SIMULATION")

for i in range(100):

    r = random.randint(1, total_stake)

    current = 0

    for node, stake in nodes.items():

        current += stake

        if r <= current:
            selected = node
            break

    count[selected] += 1

    print("Round:", i + 1, "Validator:", selected)


print("\nValidator Distribution")

for node in nodes:
    print(node, ":", count[node])

print("\nPoW requires repeated hashing.")
print("PoS selects validators based on stake.")