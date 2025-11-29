"""Persistent homology helper."""
from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np

try:
    from ripser import ripser
    from persim import plot_diagrams
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError("Install ripser and persim to use persistent homology features") from exc


def compute_diagrams(points: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute H0, H1, H2 diagrams for the provided point cloud."""
    diagrams = ripser(points, maxdim=2, coeff=2)["dgms"]
    return diagrams[0], diagrams[1], diagrams[2]


def robustness_from_h1(h1: Iterable[Tuple[float, float]]) -> float:
    """Return a bounded robustness score from H1 lifetimes."""
    finite_lifetimes = [death - birth for birth, death in h1 if death != float("inf")]
    if not finite_lifetimes:
        return 0.0
    persistent = [l for l in finite_lifetimes if l > 0.5]
    transient = [l for l in finite_lifetimes if l <= 0.5]
    late = sum(persistent)
    early = sum(transient)
    return max(0.0, min(1.0, 1.0 - early / (late + 1e-6)))


def plot(dgms) -> None:  # pragma: no cover
    plot_diagrams(dgms, show=True)
