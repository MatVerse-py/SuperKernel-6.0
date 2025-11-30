# SuperKernel 6.0 – Sovereign Prime Stack

This repository packages the MatVerse 6.x sovereign stack into runnable pieces:

* **Captals Prime Chain** – prime-based L0 with zk-validated semiprime challenges.
* **Merkle Root Identity** – deterministic identity tree builder backing the chain.
* **NegU** – neguentropy-pegged ERC-20 that breathes with Ω-score.
* **Constitutional Engine** – Hamiltonian density plus persistent homology scoring.

The immutable constitutional document remains in `SUPERKERNEL_CONSTITUTION.md` as the
canonical ceiling of the 6.x line.

## Layout

```
contracts/
  CaptalsPrimeChain.sol   # prime-chain consensus anchor
  IdentityMerkle.sol      # on-chain Merkle proof helper
  NegU.sol                # entropy-reactive ERC-20
  OracleMock.sol          # local dev oracle for Ω-score
src/
  identity/merkle_identity.py   # Keccak-256 Merkle root builder for identities
  prime_chain/block_builder.py  # block prototype wiring Merkle + prime challenge
  eng/hamiltonian_complete.py   # symbolic Hamiltonian density (tensorial)
  eng/persistent_homology.py    # ripser-based H0/H1/H2 and robustness metric
  eng/system.py                 # combines Hamiltonian + homology -> Ω-score snapshot
scripts/
  deploy_prime_chain.js         # Hardhat deployment of oracle + NegU + prime chain
hardhat.config.js               # Solidity toolchain config
package.json                    # dev dependencies + scripts
```

## Usage

### Python dependencies

```bash
pip install -r requirements.txt
```

### Build an identity Merkle root
```
python -m src.identity.merkle_identity
```

### Prototype a block off-chain
```
python -m src.prime_chain.block_builder
```

### Run the constitutional engine (requires `ripser`/`persim` installed)
```
python -m src.eng.system
```

### Deploy contracts locally (Hardhat)
```
npm install
npx hardhat compile
npm run deploy:prime
```

## Notes

* `NegU` uses an entropy oracle (mock provided) to mint/burn on Ω-score changes.
* `CaptalsPrimeChain` expects zkSNARK verification for prime challenges; the stub
  enforces only presence of proof payloads so Hardhat deployments work immediately.
* `IdentityMerkle` aligns with the off-chain builder for membership proofs.
