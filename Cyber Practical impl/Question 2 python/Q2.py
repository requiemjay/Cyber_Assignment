import hashlib
import time


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.levels = []

        if not transactions:
            self.root = ""
            return

        level = [sha256(tx) for tx in transactions]
        self.levels.append(level)

        while len(level) > 1:
            if len(level) % 2 == 1:
                level.append(level[-1])

            new_level = []

            for i in range(0, len(level), 2):
                new_level.append(sha256(level[i] + level[i + 1]))

            level = new_level
            self.levels.append(level)

        self.root = level[0]

    def get_proof(self, index):
        proof = []

        for level in self.levels[:-1]:
            if len(level) % 2 == 1:
                level.append(level[-1])

            if index % 2 == 0:
                proof.append(level[index + 1])
            else:
                proof.append(level[index - 1])

            index = index // 2

        return proof

    @staticmethod
    def verify_proof(tx, proof, root, index):
        h = sha256(tx)

        for sibling in proof:
            if index % 2 == 0:
                h = sha256(h + sibling)
            else:
                h = sha256(sibling + h)

            index = index // 2

        return h == root


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = MerkleTree(transactions).root
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (
            str(self.index) +
            str(self.timestamp) +
            str(self.transactions) +
            self.previous_hash +
            self.merkle_root +
            str(self.nonce)
        )

        return sha256(data)


class Blockchain:
    def __init__(self):
        self.chain = [Block(0, ["Genesis Block"], "0")]

    def add_block(self, transactions):
        prev = self.chain[-1]

        block = Block(
            len(self.chain),
            transactions,
            prev.hash
        )

        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.previous_hash != prev.hash:
                return False

            if curr.hash != curr.calculate_hash():
                return False

            if curr.merkle_root != MerkleTree(curr.transactions).root:
                return False

        return True


bc = Blockchain()

bc.add_block(["Alice pays Bob", "Bob pays Charlie"])
bc.add_block(["Charlie pays David", "David pays Alice"])
bc.add_block(["Alice pays Eve", "Eve pays Frank"])
bc.add_block(["Frank pays George", "George pays Alice"])

print("Blockchain created")
print("Total blocks:", len(bc.chain))
print("Chain valid:", bc.is_chain_valid())


block = bc.chain[2]

tx = block.transactions[0]
tree = MerkleTree(block.transactions)
proof = tree.get_proof(0)

result = MerkleTree.verify_proof(
    tx,
    proof,
    block.merkle_root,
    0
)

print("\nSPV Verification")
print("Transaction:", tx)
print("Merkle Root:", block.merkle_root)
print("Proof valid:", result)


bc.chain[2].transactions[0] = "Modified transaction"

print("\nAfter tampering")
print("Chain valid:", bc.is_chain_valid())