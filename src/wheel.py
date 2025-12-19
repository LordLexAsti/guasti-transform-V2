from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

@dataclass(frozen=True)
class Wheel:
    P: int
    residues: List[int]
    gaps: List[int]
    gap_of_residue: Dict[int, int]
    max_gap: int

def residues_and_gaps(P: int) -> Wheel:
    """Compute the wheel residues R(P) = {1..P : gcd(r,P)=1} and the cyclic gaps G(P)."""
    residues = [r for r in range(1, P + 1) if gcd(r, P) == 1]
    gaps = [residues[i + 1] - residues[i] for i in range(len(residues) - 1)]
    gaps.append(P + residues[0] - residues[-1])
    gap_of_residue = {residues[i]: gaps[i] for i in range(len(residues))}
    return Wheel(P=P, residues=residues, gaps=gaps, gap_of_residue=gap_of_residue, max_gap=max(gaps))
