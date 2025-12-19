from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict

import numpy as np

from .wheel import Wheel
from .features import Precomp

@dataclass(frozen=True)
class ScoreParams:
    w_s31: float = 0.40
    w_s101: float = 0.30
    w_s251: float = 0.18
    w_ang: float = 0.08
    w_gap: float = 0.04
    w_neigh: float = 0.06   # penalty
    neigh_clip_div: float = 4.0

def clip01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def score_v1_no_residue(n: int, P: int, wheel: Wheel, pre: Precomp, params: ScoreParams = ScoreParams()) -> float:
    """Score v1 (no residue prior). Candidate must satisfy gcd(n,P)=1 for intended use."""
    r = n % P
    if r == 0:
        r = P
    gap = wheel.gap_of_residue.get(r, 0)
    gap_norm = gap / wheel.max_gap if wheel.max_gap else 0.0

    c31 = int(pre.c31[n])
    c101 = int(pre.c101[n])
    c251 = int(pre.c251[n])

    s31 = 1.0 / (1.0 + c31)
    s101 = 1.0 / (1.0 + c101)
    s251 = 1.0 / (1.0 + c251)

    p = int(pre.spf_251[n])
    if p > 0:
        theta_min = math.atan(n / (p * p))
    else:
        theta_min = math.pi / 2
    ang = theta_min / (math.pi / 2)

    neigh = float(pre.sat31[n])
    neigh_term = clip01(neigh / params.neigh_clip_div)

    return (
        params.w_s31 * s31
        + params.w_s101 * s101
        + params.w_s251 * s251
        + params.w_ang * ang
        + params.w_gap * gap_norm
        - params.w_neigh * neigh_term
    )
