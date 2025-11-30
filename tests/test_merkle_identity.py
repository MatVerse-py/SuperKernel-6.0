import pytest

from src.identity.merkle_identity import (
    IdentityRecord,
    build_merkle_proof,
    build_merkle_root,
    build_merkle_proof_hex,
    build_merkle_root_hex,
    verify_merkle_proof,
    verify_merkle_proof_hex,
)
from src.identity.keccak import keccak_256


def test_merkle_root_is_deterministic():
    records = [
        IdentityRecord("0xabc", "0xdef", "0x123", 1),
        IdentityRecord("0xaaa", "0xbbb", "0xccc", 2),
        IdentityRecord("0x111", "0x222", "0x333", 3),
    ]

    root_a = build_merkle_root(records)
    root_b = build_merkle_root(records)

    assert root_a == root_b


def test_proof_matches_solidity_contract_logic():
    records = [
        IdentityRecord("0xabc", "0xdef", "0x123", 1),
        IdentityRecord("0xaaa", "0xbbb", "0xccc", 2),
        IdentityRecord("0x111", "0x222", "0x333", 3),
    ]

    target_index = 1
    target_leaf = records[target_index].to_leaf()

    proof = build_merkle_proof(records, target_index)
    root = build_merkle_root(records)

    assert verify_merkle_proof(proof, root, target_leaf)
    assert len(proof) == 2


def test_proof_input_validation():
    records = [IdentityRecord("a", "b", "c", 1)]

    with pytest.raises(IndexError):
        build_merkle_proof(records, 2)

    with pytest.raises(ValueError):
        build_merkle_proof([], 0)


def test_hex_helpers_round_trip_against_bytes_interfaces():
    records = [
        IdentityRecord("0xabc", "0xdef", "0x123", 1),
        IdentityRecord("0xaaa", "0xbbb", "0xccc", 2),
        IdentityRecord("0x111", "0x222", "0x333", 3),
    ]

    idx = 2
    root_bytes = build_merkle_root(records)
    proof_bytes = build_merkle_proof(records, idx)
    leaf_bytes = records[idx].to_leaf()

    root_hex = build_merkle_root_hex(records)
    proof_hex = build_merkle_proof_hex(records, idx)
    leaf_hex = leaf_bytes.hex()

    assert root_hex == root_bytes.hex()
    assert proof_hex == [node.hex() for node in proof_bytes]
    assert verify_merkle_proof(proof_bytes, root_bytes, leaf_bytes)
    assert verify_merkle_proof_hex(proof_hex, root_hex, leaf_hex)


def test_keccak256_matches_reference_vector():
    # Reference digest generated via Solidity's keccak256("abc")
    expected = "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"
    assert keccak_256(b"abc").hex() == expected
