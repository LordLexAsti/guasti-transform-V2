from __future__ import annotations

import argparse
import math
from typing import Iterable, List, Optional, Tuple

from .wheel import residues_and_gaps, gcd


# --- Deterministic Miller-Rabin for 64-bit ints ---
def _mr_pow(a: int, d: int, n: int) -> int:
    return pow(a, d, n)

def is_prime64(n: int) -> bool:
    """Deterministic for n < 2^64 using known bases."""
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    # write n-1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Bases valid for 64-bit determinism
    # Ref: deterministic MR bases set (first widely used set)
    bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        witness = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                witness = False
                break
        if witness:
            return False
    return True

def smallest_factor(n: int, primes: List[int]) -> int:
    if n % 2 == 0:
        return 2
    r = int(math.isqrt(n))
    for p in primes:
        if p > r:
            break
        if n % p == 0:
            return p
    return 0

def primes_upto(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:n+1:step] = b"\x00" * (((n - start) // step) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

def polarity6(n: int) -> str:
    """Return 'D' if n ≡ 1 (mod 6), 'G' if n ≡ 5 (mod 6), '-' otherwise."""
    r = n % 6
    if r == 1:
        return "D"
    if r == 5:
        return "G"
    return "-"

def signature_small(n: int) -> Tuple[int, int, int]:
    """Return a reduced residue signature (mod 5,7,11) for quick annotation."""
    return (n % 5, n % 7, n % 11)

def parse_rays(s: str) -> List[int]:

    if not s:
        return []
    parts = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    return [int(x) for x in parts]

def classify(n: int, rays: List[int], trial_primes: List[int]) -> Tuple[str, Optional[int]]:
    """Return ('prime'|'composite', factor_or_None)."""
    if n < 2:
        return ("composite", None)
    # Fast ray check first (educational)
    for p in rays:
        if p > 1 and n % p == 0:
            return ("composite", p)
    # Definitive primality
    if is_prime64(n):
        return ("prime", None)
    # Optional: show smallest factor (nice for ASCII)
    f = smallest_factor(n, trial_primes)
    return ("composite", f if f else None)

def tower(P: int, m: int, span: int, rays: List[int], max_print: int, show_polarity: bool, show_signature: bool) -> None:
    center = P * m
    # trial primes for factor display (sqrt(center+span))
    trial_primes = primes_upto(int(math.isqrt(center + span)) + 1)

    candidates: List[Tuple[int, int, str, Optional[int]]] = []
    for n in range(center - span, center + span + 1):
        if n == center:
            continue
        if gcd(n, P) != 1:
            continue
        side = n - center  # negative left, positive right
        status, f = classify(n, rays=rays, trial_primes=trial_primes)
        candidates.append((side, n, status, f))

    # Sort by distance from center (|side|), then left before right for same |side|
    candidates.sort(key=lambda t: (abs(t[0]), t[0]))

    print(f"\nTAMIS ANGULAIRE — mod {P} — centre = {center} (= {P}×{m}) — span = ±{span}")
    print(f"Balcons (candidats): gcd(n,{P})=1  |  Rayons surveillés: {rays if rays else '—'}")
    print("Légende: 💎 premier (MR déterministe 64-bit), 💥 composé, ⇠ facteur détecté")
    if show_polarity:
        print("Polarité mod 6: χ6=D si n≡1 (mod6), χ6=G si n≡5 (mod6) (sinon -).")
    if show_signature:
        print("Signature réduite: (n mod 5, n mod 7, n mod 11) pour annotation rapide.")
    print()

    shown = 0
    for side, n, status, f in candidates:
        if shown >= max_print:
            break
        if status == "prime":
            mark = "💎"
            extra = ""
        else:
            mark = "💥"
            extra = f" ⇠ {f}" if f else ""
        lr = "G" if side < 0 else "D"
        r = n % P
        r = P if r == 0 else r
        fields = [
            f"{lr} {side:>6}",
            f"n={n:<10}",
            f"r={r:>4}",
        ]
        if show_polarity:
            fields.append(f"χ6={polarity6(n)}")
        if show_signature:
            s5, s7, s11 = signature_small(n)
            fields.append(f"(5,7,11)=({s5},{s7},{s11})")
        fields.append(f"{mark}{extra}")
        print(" | ".join(fields))
        shown += 1

    if shown == 0:
        print("(Aucun balcon dans cette fenêtre.)")

def respiration(P: int, k: int) -> None:
    w = residues_and_gaps(P)
    residues = w.residues
    gaps = w.gaps
    print(f"\nRESPIRATION — mod {P} — φ(P)={len(residues)} — gap_max={w.max_gap}")
    kk = min(k, len(residues))
    print("Début des résidus:")
    print(residues[:kk])
    print("Début des gaps:")
    print(gaps[:kk])
    print(f"(Somme gaps = {sum(gaps)})")

def main() -> None:
    ap = argparse.ArgumentParser(description="ASCII 'tamis angulaire' tower visualizer (mod 30 / mod 2310 etc.).")
    ap.add_argument("--P", type=int, default=30, help="Modulus P (e.g. 30, 210, 2310). Default 30.")
    ap.add_argument("--m", type=int, default=1, help="Center multiplier: center = P*m. Default 1.")
    ap.add_argument("--span", type=int, default=60, help="Half-width around center (±span). Default 60.")
    ap.add_argument("--rays", type=str, default="7,11,13,17,19,23", help="Comma-separated ray primes to flag (optional).")
    ap.add_argument("--max-print", type=int, default=120, help="Max balconies to print. Default 120.")
    ap.add_argument("--show-respiration", action="store_true", help="Also print beginning of the respiration (residues+gaps).")
    ap.add_argument("--show-polarity", action="store_true", help="Show polarity χ6 (G/D) for candidates when applicable.")
    ap.add_argument("--show-signature", action="store_true", help="Show reduced signature (mod 5,7,11) for quick annotation.")
    ap.add_argument("--resp-k", type=int, default=24, help="How many residues/gaps to print if --show-respiration.")
    args = ap.parse_args()

    rays = parse_rays(args.rays)
    if args.show_respiration:
        respiration(args.P, args.resp_k)
    tower(P=args.P, m=args.m, span=args.span, rays=rays, max_print=args.max_print, show_polarity=args.show_polarity, show_signature=args.show_signature)

if __name__ == "__main__":
    main()
