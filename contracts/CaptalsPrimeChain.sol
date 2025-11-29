// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

/// @title CaptalsPrimeChain
/// @notice Sovereign prime-based chain anchoring identity via Merkle roots.
/// Prime challenges are validated with a zk-proof of semiprime factorisation.
contract CaptalsPrimeChain {
    struct PrimeChallenge {
        bytes n; // 2048-bit semiprime encoded as bytes
        bytes p; // 1024-bit prime factor
        bytes q; // 1024-bit prime factor
        bytes zkProof; // zkSNARK attesting p * q = n
    }

    struct Block {
        uint256 blockNumber;
        bytes32 previousHash;
        uint256 timestamp;
        PrimeChallenge primeChallenge;
        bytes32 merkleRootIdentity;
        bytes32 stateRoot;
    }

    event BlockSubmitted(uint256 indexed blockNumber, bytes32 indexed previousHash, bytes32 merkleRootIdentity, bytes32 stateRoot);

    Block[] public chain;

    /// @param previousHash Hash of previous block (or 0x0 for genesis).
    /// @param merkleRootIdentity SHA3-256 Merkle root of identity tree.
    /// @param stateRoot Poseidon hash of state commitment.
    /// @param primeChallenge Encoded semiprime challenge and zk proof.
    function submitBlock(
        bytes32 previousHash,
        bytes32 merkleRootIdentity,
        bytes32 stateRoot,
        PrimeChallenge calldata primeChallenge
    ) external {
        require(_isPrimeProofValid(primeChallenge), "Invalid prime proof");

        uint256 newNumber = chain.length;
        chain.push(
            Block({
                blockNumber: newNumber,
                previousHash: previousHash,
                timestamp: block.timestamp,
                primeChallenge: primeChallenge,
                merkleRootIdentity: merkleRootIdentity,
                stateRoot: stateRoot
            })
        );

        emit BlockSubmitted(newNumber, previousHash, merkleRootIdentity, stateRoot);
    }

    /// @notice Returns block details.
    function getBlock(uint256 index) external view returns (Block memory) {
        return chain[index];
    }

    /// @dev Placeholder for zkSNARK verification of prime factors.
    function _isPrimeProofValid(PrimeChallenge calldata primeChallenge) internal pure returns (bool) {
        // Integrate circom/snarkjs generated verifier here.
        return primeChallenge.zkProof.length > 0 && primeChallenge.n.length > 0 && primeChallenge.p.length > 0 && primeChallenge.q.length > 0;
    }
}
