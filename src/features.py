from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import List, Sequence, Tuple

def sieve_is_prime(n: int) -> np.ndarray:
    """Boolean sieve: is_prime[x] for x in [0..n]."""
    is_prime = np.ones(n + 1, dtype=bool)
    if n >= 0:
        is_prime[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i : n+1 : i] = False
    return is_prime

def primes_upto(n: int) -> List[int]:
    mask = sieve_is_prime(n)
    return np.nonzero(mask)[0].tolist()

@dataclass
class Precomp:
    B: int
    primes_251: List[int]
    spf_251: np.ndarray         # smallest prime factor <=251, else 0
    c31: np.ndarray
    c101: np.ndarray
    c251: np.ndarray
    sat31: np.ndarray           # neighborhood saturation (mean c31 on n±w)
    is_prime: np.ndarray        # sieve up to B

def build_precomp(B: int, w: int = 3) -> Precomp:
    """Precompute arrays needed for fast scoring up to B."""
    is_prime = sieve_is_prime(B)
    primes_251 = primes_upto(251)

    spf = np.zeros(B + 1, dtype=np.int32)
    for p in primes_251:
        spf[p : B + 1 : p] = np.where(spf[p : B + 1 : p] == 0, p, spf[p : B + 1 : p])

    c31 = np.zeros(B + 1, dtype=np.int16)
    c101 = np.zeros(B + 1, dtype=np.int16)
    c251 = np.zeros(B + 1, dtype=np.int16)

    for p in primes_251:
        if p <= 31:
            c31[p : B + 1 : p] += 1
            c101[p : B + 1 : p] += 1
            c251[p : B + 1 : p] += 1
        elif p <= 101:
            c101[p : B + 1 : p] += 1
            c251[p : B + 1 : p] += 1
        else:
            c251[p : B + 1 : p] += 1

    # sat31 via prefix sums
    prefix = np.zeros(B + 2, dtype=np.int32)
    prefix[1:] = np.cumsum(c31, dtype=np.int32)

    sat31 = np.zeros(B + 1, dtype=np.float32)
    for n in range(1, B + 1):
        lo = max(1, n - w)
        hi = min(B, n + w)
        sat31[n] = (prefix[hi + 1] - prefix[lo]) / (hi - lo + 1)

    return Precomp(
        B=B,
        primes_251=primes_251,
        spf_251=spf,
        c31=c31,
        c101=c101,
        c251=c251,
        sat31=sat31,
        is_prime=is_prime,
    )
