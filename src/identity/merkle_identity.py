"""Identity Merkle tree builder for Captals Prime Chain.

Each identity couples biometric and digital material and is hashed into a
Keccak-256 leaf (the same primitive Solidity exposes through ``keccak256``).
The resulting Merkle root is submitted to the chain and later proved with
on-chain proofs through the ``IdentityMerkle`` library.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, List

from Crypto.Hash import keccak


def _strip_0x(hex_string: str) -> str:
    """Remove a leading ``0x`` from a hex string when present."""

    return hex_string[2:] if hex_string.startswith("0x") else hex_string


def _keccak_bytes(payload: bytes) -> bytes:
    """Return the Keccak-256 digest for raw bytes."""

    return keccak.new(data=payload, digest_bits=256).digest()


def _hash_pair(left: bytes, right: bytes) -> bytes:
    """Hash an ordered pair of nodes to mirror Solidity's ``keccak256`` tree.

    Solidity's ``IdentityMerkle.verify`` sorts each sibling pair before hashing;
    we mirror that here so off-chain roots and proofs match on-chain checks.
    """

    if left > right:
        left, right = right, left
    return _keccak_bytes(left + right)


@dataclass
class IdentityRecord:
    biometric_hash: str
    digital_pubkey: str
    metadata_hash: str
    nonce: int

    def to_leaf(self) -> bytes:
        serialized = json.dumps(
            {
                "biometric_hash": self.biometric_hash,
                "digital_pubkey": self.digital_pubkey,
                "metadata_hash": self.metadata_hash,
                "nonce": self.nonce,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return _keccak_bytes(serialized.encode())


def build_merkle_root(records: Iterable[IdentityRecord]) -> bytes:
    """Compute a Keccak-256 Merkle root for the provided identities."""
    leaves: List[bytes] = [record.to_leaf() for record in records]
    if not leaves:
        raise ValueError("At least one identity is required to build a Merkle root")

    level = leaves
    while len(level) > 1:
        next_level: List[bytes] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            next_level.append(_hash_pair(left, right))
        level = next_level
    return level[0]


def build_merkle_proof(records: Iterable[IdentityRecord], index: int) -> List[bytes]:
    """Generate a Merkle inclusion proof for the record at ``index``.

    The proof ordering matches ``IdentityMerkle.verify`` (ordered hashing).
    """

    leaves: List[bytes] = [record.to_leaf() for record in records]
    if not leaves:
        raise ValueError("At least one identity is required to build a Merkle proof")
    if index < 0 or index >= len(leaves):
        raise IndexError("Index out of range for provided identities")

    level = leaves
    proof: List[bytes] = []
    idx = index

    while len(level) > 1:
        next_level: List[bytes] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left

            if i == idx - (idx % 2):
                sibling = right if idx % 2 == 0 else left
                proof.append(sibling)

            next_level.append(_hash_pair(left, right))

        level = next_level
        idx //= 2

    return proof


def build_merkle_root_hex(records: Iterable[IdentityRecord]) -> str:
    """Compute a Merkle root and return it as a hex string without ``0x``."""

    return build_merkle_root(records).hex()


def build_merkle_proof_hex(records: Iterable[IdentityRecord], index: int) -> List[str]:
    """Return a Merkle proof encoded as hex strings without ``0x``."""

    return [node.hex() for node in build_merkle_proof(records, index)]


def verify_merkle_proof(proof: Iterable[bytes], root: bytes, leaf: bytes) -> bool:
    """Verify a Merkle proof using the same ordering rule as the Solidity helper."""

    computed = leaf
    for sibling in proof:
        if computed <= sibling:
            computed = _hash_pair(computed, sibling)
        else:
            computed = _hash_pair(sibling, computed)
    return computed == root


def verify_merkle_proof_hex(proof_hex: Iterable[str], root_hex: str, leaf_hex: str) -> bool:
    """Verify a hex-encoded proof and root using the Solidity-compatible hashing rule."""

    proof_bytes = [bytes.fromhex(_strip_0x(sibling)) for sibling in proof_hex]
    root_bytes = bytes.fromhex(_strip_0x(root_hex))
    leaf_bytes = bytes.fromhex(_strip_0x(leaf_hex))
    return verify_merkle_proof(proof_bytes, root_bytes, leaf_bytes)


def demo_root() -> str:
    """Return a hex Merkle root for three sample identity records."""
    sample = [
        IdentityRecord("0xabc", "0xdef", "0x123", 1),
        IdentityRecord("0xaaa", "0xbbb", "0xccc", 2),
        IdentityRecord("0x111", "0x222", "0x333", 3),
    ]
    return build_merkle_root(sample).hex()


if __name__ == "__main__":
    print("Sample Merkle root:", demo_root())
