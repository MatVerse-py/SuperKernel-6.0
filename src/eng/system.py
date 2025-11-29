"""Integrated constitutional engine combining Hamiltonian and homology."""
from __future__ import annotations

import numpy as np

from src.eng.hamiltonian_complete import HamiltonianComplete
from src.eng.persistent_homology import compute_diagrams, robustness_from_h1


class ConstitutionalEngine:
    def __init__(self) -> None:
        self.hamiltonian = HamiltonianComplete()

    def evaluate(self, points: np.ndarray) -> dict:
        """Evaluate Hamiltonian density symbolically and homology robustness numerically."""
        h_density = self.hamiltonian.pretty()
        h0, h1, h2 = compute_diagrams(points)
        omega_score = robustness_from_h1(h1)
        return {"hamiltonian_density": h_density, "omega": omega_score, "h0": h0, "h1": h1, "h2": h2}


if __name__ == "__main__":
    sample_points = np.random.rand(128, 3)
    engine = ConstitutionalEngine()
    summary = engine.evaluate(sample_points)
    print({"omega": summary["omega"], "hamiltonian_density": summary["hamiltonian_density"]})
