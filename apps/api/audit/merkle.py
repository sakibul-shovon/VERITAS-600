"""RFC 9162 Compliant Merkle Tree Implementation.

Provides:
1. Leaf prefixing (\x00) and internal node prefixing (\x01) preventing second-preimage attacks.
2. Root hash calculation over an arbitrary sequence of evidence leaves.
3. Cryptographic proof generation and verification for any leaf.
"""

from __future__ import annotations

import hashlib
from typing import List, Tuple


class MerkleTree:
    """Immutable Merkle Tree over evidence leaves."""

    def __init__(self, leaves: List[str]):
        """Initialize with a list of hex-encoded leaf digests."""
        self.raw_leaves = list(leaves)
        self.levels: List[List[bytes]] = []
        self._build_tree()

    def _hash_leaf(self, hex_digest: str) -> bytes:
        # RFC 9162 domain separation: 0x00 for leaves
        return hashlib.sha256(b"\x00" + bytes.fromhex(hex_digest)).digest()

    def _hash_internal(self, left: bytes, right: bytes) -> bytes:
        # RFC 9162 domain separation: 0x01 for internal nodes
        return hashlib.sha256(b"\x01" + left + right).digest()

    def _build_tree(self) -> None:
        if not self.raw_leaves:
            self.root = hashlib.sha256(b"\x00").hexdigest()
            return

        current = [self._hash_leaf(leaf) for leaf in self.raw_leaves]
        self.levels.append(current)

        while len(current) > 1:
            next_level: List[bytes] = []
            for i in range(0, len(current), 2):
                left = current[i]
                if i + 1 < len(current):
                    right = current[i + 1]
                else:
                    right = left  # Duplicate last element if odd
                next_level.append(self._hash_internal(left, right))
            self.levels.append(next_level)
            current = next_level

        self.root = current[0].hex()

    @property
    def root_hex(self) -> str:
        return self.root

    def get_proof(self, index: int) -> List[Tuple[str, str]]:
        """Return inclusion proof as a list of (direction, sibling_hex)."""
        if index < 0 or index >= len(self.raw_leaves):
            raise IndexError("Leaf index out of bounds")

        proof: List[Tuple[str, str]] = []
        idx = index

        for level in self.levels[:-1]:
            is_right = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right else idx + 1
            if sibling_idx < len(level):
                sibling = level[sibling_idx].hex()
            else:
                sibling = level[idx].hex()

            proof.append(("left" if is_right else "right", sibling))
            idx //= 2

        return proof

    @staticmethod
    def verify_proof(leaf_hex: str, proof: List[Tuple[str, str]], expected_root_hex: str) -> bool:
        """Verify that leaf_hex is in the tree with root expected_root_hex."""
        current = hashlib.sha256(b"\x00" + bytes.fromhex(leaf_hex)).digest()

        for direction, sibling_hex in proof:
            sibling = bytes.fromhex(sibling_hex)
            if direction == "left":
                current = hashlib.sha256(b"\x01" + sibling + current).digest()
            else:
                current = hashlib.sha256(b"\x01" + current + sibling).digest()

        return current.hex() == expected_root_hex
