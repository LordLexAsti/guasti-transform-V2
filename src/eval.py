from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

from .wheel import residues_and_gaps, gcd
from .features import build_precomp
from .score import score_v1_no_residue, ScoreParams

def candidate_mask(B: int, prime_factors: Sequence[int]) -> np.ndarray:
    """Mask of n in [0..B] that are coprime with P (exclude multiples of prime factors)."""
    mask = np.ones(B + 1, dtype=bool)
    mask[:2] = False
    mask[1] = False
    for q in prime_factors:
        mask[q : B + 1 : q] = False
    return mask

def factorize_squarefree(P: int) -> List[int]:
    """Return distinct prime factors of P (works for squarefree primorials)."""
    pf = []
    x = P
    d = 2
    while d * d <= x:
        if x % d == 0:
            pf.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        pf.append(x)
    return pf

def precision_at(df_is_prime: np.ndarray, ks: Sequence[int]) -> Dict[int, float]:
    out = {}
    n = len(df_is_prime)
    for k in ks:
        kk = min(k, n)
        out[k] = float(df_is_prime[:kk].mean()) if kk > 0 else float('nan')
    return out

def run_window(P: int, A: int, B: int, w: int, ks: Sequence[int]) -> Dict[str, float]:
    """Compute base rate and P@K for one window [A..B]."""
    wheel = residues_and_gaps(P)
    prime_factors = factorize_squarefree(P)

    pre = build_precomp(B, w=w)
    cand = candidate_mask(B, prime_factors)

    scores = []
    labels = []
    for n in range(A, B + 1):
        if not cand[n]:
            continue
        s = score_v1_no_residue(n, P=P, wheel=wheel, pre=pre)
        scores.append(s)
        labels.append(bool(pre.is_prime[n]))

    if not scores:
        return {
            "candidates": 0,
            "base_rate": float("nan"),
            **{f"P@{k}": float("nan") for k in ks},
        }

    scores = np.asarray(scores, dtype=np.float64)
    labels = np.asarray(labels, dtype=bool)

    order = np.argsort(-scores)  # descending
    labels_sorted = labels[order]

    base_rate = float(labels_sorted.mean())
    prec = precision_at(labels_sorted, ks)

    return {
        "candidates": int(labels_sorted.size),
        "base_rate": base_rate,
        **{f"P@{k}": prec[k] for k in ks},
    }

def main():
    ap = argparse.ArgumentParser(description="Guasti score v1 (P primorial) evaluation.")
    ap.add_argument("--P", type=int, default=2310, help="Wheel modulus (primorial), default 2310.")
    ap.add_argument("--A", type=int, default=500001, help="Window start (inclusive).")
    ap.add_argument("--B", type=int, default=1000000, help="Window end (inclusive).")
    ap.add_argument("--w", type=int, default=3, help="Neighborhood radius for sat31, default 3.")
    ap.add_argument("--K", type=int, nargs="+", default=[100, 500, 1000, 5000, 20000], help="List of K for Precision@K.")
    ap.add_argument("--windows", type=int, nargs="*", default=None,
                   help="Optional list of window pairs: A1 B1 A2 B2 ... Overrides --A/--B if provided.")
    args = ap.parse_args()

    if args.windows:
        if len(args.windows) % 2 != 0:
            raise SystemExit("--windows expects an even number of integers: A1 B1 A2 B2 ...")
        pairs = [(args.windows[i], args.windows[i+1]) for i in range(0, len(args.windows), 2)]
    else:
        pairs = [(args.A, args.B)]

    print(f"P={args.P}  w={args.w}  K={args.K}")
    for (A, B) in pairs:
        res = run_window(P=args.P, A=A, B=B, w=args.w, ks=args.K)
        head = f"[{A}-{B}] candidates={res['candidates']:,} base_rate={res['base_rate']:.6f}"
        print(head)
        for k in args.K:
            print(f"  P@{k}: {res[f'P@{k}']:.6f}")
        print()

if __name__ == "__main__":
    main()
