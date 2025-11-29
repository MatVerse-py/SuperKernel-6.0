"""Hamiltonian density for the sovereign MatVerse kernel."""
from __future__ import annotations

import sympy as sp


class HamiltonianComplete:
    """Symbolic Hamiltonian capturing kinetic, constitutional and field terms."""

    def __init__(self) -> None:
        x0, x1, x2 = sp.symbols("x0 x1 x2", real=True)
        psi = sp.Function("Psi")(x0, x1, x2)
        psi_conj = sp.Function("Psi_c")(x0, x1, x2)

        sigma_z = sp.Matrix([[1, 0], [0, -1]])
        rho_hat = sp.Matrix([[psi * psi_conj, 0], [0, psi_conj * psi]])
        tr_sigma_rho = sp.trace(sigma_z * rho_hat)

        g = sp.diag(1, 1, 1)
        g_inv = g.inv()
        grad = [sp.diff(psi, x0), sp.diff(psi, x1), sp.diff(psi, x2)]
        kinetic = sum(g_inv[i, j] * grad[i] * grad[j] for i in range(3) for j in range(3))

        omega = sp.Function("Omega")(x0, x1, x2)
        field = omega ** 2

        self.h_density = sp.sqrt(g.det()) * (tr_sigma_rho + kinetic + field)

    def pretty(self) -> str:
        return sp.simplify(self.h_density).__repr__()


if __name__ == "__main__":
    h = HamiltonianComplete()
    print("H_density =", h.pretty())
