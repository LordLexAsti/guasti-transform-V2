# tests/test_invariants.py
import math

import pytest

from src.wheel import gcd, residues_and_gaps
from src.eval import factorize_squarefree, candidate_mask, run_window


@pytest.mark.parametrize("P", [30, 210, 2310])
def test_wheel_invariants(P: int):
    w = residues_and_gaps(P)

    assert w.P == P
    assert w.residues == sorted(w.residues)
    assert len(w.residues) == len(set(w.residues))

    # φ(P) attendu (ok car P est squarefree ici: primorial)
    phi = P
    for p in factorize_squarefree(P):
        phi = phi // p * (p - 1)
    assert len(w.residues) == phi

    # Tous copremiers
    assert all(gcd(r, P) == 1 for r in w.residues)

    # Gaps cycliques cohérents
    assert len(w.gaps) == len(w.residues)
    assert sum(w.gaps) == P
    assert w.max_gap == max(w.gaps)

    # Dictionnaire résidu -> gap
    assert set(w.gap_of_residue.keys()) == set(w.residues)
    assert all(w.gap_of_residue[r] > 0 for r in w.residues)


def side_mod6(n: int) -> int | None:
    # -1 = 6k-1 (≡ 5), +1 = 6k+1 (≡ 1)
    r = n % 6
    if r == 5:
        return -1
    if r == 1:
        return +1
    return None


def test_polarity_mod6_multiplication_law():
    # Vérifie la “loi de polarité” en mod 6 sur un échantillon
    cands = [n for n in range(5, 500) if gcd(n, 6) == 1]  # ≡1 ou ≡5

    for a in cands:
        for b in cands:
            sa = side_mod6(a)
            sb = side_mod6(b)
            assert sa in (-1, +1) and sb in (-1, +1)

            prod = (a * b) % 6
            # le produit est forcément ≡1 ou ≡5
            assert prod in (1, 5)

            # règle des signes : (-)(-)=(+), (+)(+)=(+), (-)(+) = (-)
            expected = +1 if (sa == sb) else -1
            got = +1 if prod == 1 else -1
            assert got == expected


def test_candidate_mask_excludes_prime_factors():
    P = 2310
    pf = factorize_squarefree(P)
    B = 5000
    mask = candidate_mask(B, pf)

    # doit exclure multiples des facteurs de P
    for p in pf:
        assert mask[p] is False
        assert mask[2 * p] is False

    # et garder des copremiers (ex: 1 est forcé False par design, donc on teste 13)
    assert gcd(13, P) == 1
    assert mask[13] is True


def test_run_window_smoke_small():
    # smoke test (petite fenêtre) : ça tourne et renvoie des nombres
    res = run_window(P=2310, A=1000, B=5000, w=3, ks=[100, 500])
    assert res["candidates"] > 0
    assert math.isfinite(res["base_rate"])
    assert math.isfinite(res["P@100"])
    assert math.isfinite(res["P@500"])
