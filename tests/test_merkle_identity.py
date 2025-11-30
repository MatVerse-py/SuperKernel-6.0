import pytest

from src.identity.merkle_identity import (
    IdentityRecord,
    build_merkle_proof,
    build_merkle_root,
    verify_merkle_proof,
)


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
