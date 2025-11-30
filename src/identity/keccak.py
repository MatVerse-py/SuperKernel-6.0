"""Pure-Python Keccak-256 implementation to avoid external dependencies.

This module implements the Keccak-f[1600] permutation and sponge construction
needed for ``keccak256`` hashing (as exposed by Solidity). It is intentionally
minimal to keep the identity Merkle tooling self-contained when package
installation behind a proxy is not possible.
"""
from __future__ import annotations

from typing import List

# Rotation offsets for the Rho step by (x, y)
_RHO_OFFSETS = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]

# Round constants for the Iota step
_ROUND_CONSTANTS = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008,
]


def _rotl(value: int, shift: int) -> int:
    """Rotate a 64-bit integer left by ``shift`` bits."""

    return ((value << shift) & 0xFFFFFFFFFFFFFFFF) | (value >> (64 - shift))


def _keccak_f(state: List[List[int]]) -> None:
    """Apply the Keccak-f[1600] permutation in place."""

    for round_constant in _ROUND_CONSTANTS:
        # Theta
        c = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rotl(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                state[x][y] ^= d[x]

        # Rho and Pi
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = _rotl(state[x][y], _RHO_OFFSETS[x][y])

        # Chi
        for x in range(5):
            for y in range(5):
                state[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y])

        # Iota
        state[0][0] ^= round_constant


def keccak_256(data: bytes) -> bytes:
    """Return the Keccak-256 digest for ``data``.

    Implements the sponge construction with a 1088-bit rate and 512-bit
    capacity, matching the parameters used by Solidity's ``keccak256``.
    """

    rate_bytes = 136  # 1088-bit rate
    state = [[0] * 5 for _ in range(5)]  # 1600-bit state as 25 lanes of 64 bits

    # Absorb phase with pad10*1 padding
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % rate_bytes != rate_bytes - 1:
        padded.append(0x00)
    padded.append(0x80)

    for offset in range(0, len(padded), rate_bytes):
        block = padded[offset : offset + rate_bytes]
        for i in range(rate_bytes // 8):
            lane = int.from_bytes(block[8 * i : 8 * (i + 1)], "little")
            x = i % 5
            y = i // 5
            state[x][y] ^= lane
        _keccak_f(state)

    # Squeeze phase
    output = bytearray()
    while len(output) < 32:
        for i in range(rate_bytes // 8):
            x = i % 5
            y = i // 5
            output.extend(state[x][y].to_bytes(8, "little"))
        if len(output) >= 32:
            break
        _keccak_f(state)

    return bytes(output[:32])


__all__ = ["keccak_256"]
