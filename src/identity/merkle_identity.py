"""Identity Merkle tree builder for Captals Prime Chain.

Each identity couples biometric and digital material and is hashed into a
SHA3-256 leaf. The resulting Merkle root is submitted to the chain and later
proved with on-chain proofs through the IdentityMerkle library.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable, List


def _sha3_hex(payload: str) -> str:
    return hashlib.sha3_256(payload.encode()).hexdigest()


def _sha3_bytes(payload: bytes) -> bytes:
    return hashlib.sha3_256(payload).digest()


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
        return _sha3_bytes(serialized.encode())


def build_merkle_root(records: Iterable[IdentityRecord]) -> bytes:
    """Compute a SHA3-256 Merkle root for the provided identities."""
    leaves: List[bytes] = [record.to_leaf() for record in records]
    if not leaves:
        raise ValueError("At least one identity is required to build a Merkle root")

    level = leaves
    while len(level) > 1:
        next_level: List[bytes] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            combined = hashlib.sha3_256(left + right).digest()
            next_level.append(combined)
        level = next_level
    return level[0]


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
