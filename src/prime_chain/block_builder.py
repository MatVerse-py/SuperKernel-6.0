"""Prototype block builder for Captals Prime Chain."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from time import time
from typing import Dict

from src.identity.merkle_identity import IdentityRecord, build_merkle_root


@dataclass
class PrimeChallenge:
    n: str
    p: str
    q: str
    zk_proof: str

    def to_json(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class CaptalsBlock:
    block_number: int
    previous_hash: str
    timestamp: int
    prime_challenge: PrimeChallenge
    merkle_root_identity: str
    state_root: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=2)


def build_block(block_number: int, previous_hash: str) -> CaptalsBlock:
    identities = [
        IdentityRecord("0xface", "0xkey1", "0xmeta1", 7),
        IdentityRecord("0xcafe", "0xkey2", "0xmeta2", 8),
    ]
    merkle_root = build_merkle_root(identities).hex()
    challenge = PrimeChallenge(
        n="0x" + "ab" * 256,
        p="0x" + "cd" * 128,
        q="0x" + "ef" * 128,
        zk_proof="0x" + "00" * 64,
    )
    return CaptalsBlock(
        block_number=block_number,
        previous_hash=previous_hash,
        timestamp=int(time()),
        prime_challenge=challenge,
        merkle_root_identity="0x" + merkle_root,
        state_root="0x" + "12" * 32,
    )


if __name__ == "__main__":
    block = build_block(1, "0xabc123")
    print(block.to_json())
