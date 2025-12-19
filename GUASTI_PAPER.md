# GUASTI_PAPER.md
## Guasti Grid / Angular Sieve — A Discrete Geometric Re-description of Divisibility
### Version “paper” (sèche, style soumission)

> **Scope** : visualization + experimental framework for candidate filtering/scoring of primes using modular structure (6 and primorial wheels).  
> **Non-claim** : no proof of RH; no redefinition of primality.

---

## Abstract
We present a discrete, grid-based representation of divisibility (Guasti Grid) where each integer is characterized by its divisor signature. This supports an “angular sieve” interpretation: composites correspond to intersection/convergence events of divisor rays, while primes appear as structurally silent coordinates (no non-trivial intersections). We formalize the mod 6 pillar/corridor decomposition, introduce a polarity algebra on the two residue classes \(6k\pm1\), and define a “breathing pattern” (cycle of gaps) for primorial wheels \(P\in\{30,210,2310,\dots\}\). The framework yields falsifiable tests: invariants (gap sums, Euler totient cardinality, square exclusion), predictive lift vs baselines, and robustness on disjoint intervals.

---

## 1. Definitions

### 1.1 Guasti Grid (divisibility grid)
For integers \(k,n\ge 1\), define a binary grid:
\[
G(k,n)=1 \iff k\mid n.
\]
Column \(n\) encodes the divisor set of \(n\). The diagonal \((n,n)\) is an identity diagonal (labels \(n\)), not a “square diagonal” in the Pythagorean sense.

### 1.2 Candidate corridors (mod 6)
For primes \(p>3\):
\[
p\equiv 1 \pmod 6 \quad \text{or}\quad p\equiv 5 \pmod 6.
\]
Multiples of 6 are “pillars” (structural axis), and candidates lie in the two corridors \(6k\pm1\).

### 1.3 Polarity algebra (mod 6)
Define polarity for \(\gcd(n,6)=1\):
- Right (D) if \(n\equiv 1\pmod 6\),
- Left (G) if \(n\equiv 5\pmod 6\).

Then:
- \(G\cdot G \to D\),
- \(D\cdot D \to D\),
- \(G\cdot D \to G\).

Invariant:
\[
\gcd(n,6)=1 \Rightarrow n^2\equiv 1\pmod 6,
\]
hence no square \(m^2\) (with \(\gcd(m,6)=1\)) lies in the left corridor \(6k-1\).

### 1.4 Primorial wheel and breathing pattern
Let \(P=\prod_{p\le q}p\) (primorial). Define the reduced residue system:
\[
R(P)=\{r\in[1,P] : \gcd(r,P)=1\}.
\]
Sort \(R(P)\) and define the cyclic gap sequence (“breathing pattern”) \(\mathcal{G}(P)\) as successive differences, including the wrap-around gap. Invariants:
- \(|R(P)|=\varphi(P)\),
- \(\sum \mathcal{G}(P)=P\).

For window \([A,B]\), wheel candidates:
\[
C(P;A,B)=\{n\in[A,B] : \gcd(n,P)=1\}.
\]

---

## 2. Operational interpretation (Angular Sieve)
Composites correspond to non-trivial divisor intersections (multiple active rows in column \(n\)), while primes correspond to minimal signatures (only 1 and \(n\)). The corridor/polarity structure provides a coarse geometry; the wheel breathing pattern provides multi-scale periodic scaffolding.

We distinguish classical arithmetic truth from operational roles: in this framework, 2 and 3 act as structural filters (“architects”) by enforcing parity and mod 6 pillars, without changing primality definitions.

---

## 3. Experimental protocol

### 3.1 Ground truth
For each \(n\) in candidate sets, determine primality using:
- exact sieve for small windows, or
- deterministic 64-bit Miller–Rabin bases for large windows.

### 3.2 Scoring function
Define a score \(S(n)\) (to be specified by implementations) that ranks candidates using:
- polarity (G/D),
- wheel residue position (index within \(\mathcal{G}(P)\)),
- predicted impact events (e.g., onset at \(p^2\) for newly introduced rays),
- optional signature features (divisor-pattern-derived).

### 3.3 Baselines
- Baseline-6: \(6k\pm1\) in natural order,
- Baseline-wheel: \(C(P;A,B)\) in natural order,
- Random: random permutation of the same candidate list.

### 3.4 Metrics
- Prime density on a set \(X\): \(\pi(X)/|X|\),
- Precision@k on top-k ranked by \(S\),
- Lift against Baseline-wheel:
\[
\text{lift}=\frac{\text{density(top subset)}}{\text{density(baseline subset)}}.
\]

---

## 4. Falsifiable claims (hostile-ready)

### Claim 1 (Invariant breathing pattern)
For each \(P\), \(|\mathcal{G}(P)|=\varphi(P)\) and \(\sum\mathcal{G}(P)=P\).  
**Refutation**: any counterexample indicates definition/implementation failure.

### Claim 2 (Square exclusion in Left corridor)
For \(\gcd(m,6)=1\), \(m^2\equiv 1\pmod 6\).  
**Refutation**: finding \(m^2\equiv 5\pmod 6\) is impossible; failure indicates coding error.

### Claim 3 (Novel impact onset at \(p^2\))
When adding a ray \(p\ge 5\) to the model, qualitatively new self-intersection effects start at \(p^2\).  
**Refutation**: systematic “new effects” attributed to \(p\) well below \(p^2\) without coherent decomposition by smaller factors.

### Claim 4 (Predictive advantage beyond wheel)
On large disjoint windows for fixed \(P\) (e.g., \(P=2310\)), the score must provide stable lift:
- lift(top 1%) > 1.05,
- lift(top 5%) > 1.02 (thresholds adjustable but must be >1).
**Refutation**: lift ≈ 1 (or <1) across windows → no predictive power beyond wheel ordering.

### Claim 5 (Robustness across disjoint intervals)
Lift and Precision@k must remain stable across multiple disjoint windows.  
**Refutation**: effects only on cherry-picked windows.

### Negative control: “without residues”
Disable wheel residue information (no mod \(P\) features) and re-run.  
**Expected**: performance collapses toward Baseline-6 / Baseline-wheel.  
If not, suspect leakage or implicit wheel reconstruction.

---

## 5. Discussion and limitations
This framework can be valuable as:
- a pedagogical visualization (divisor signatures),
- an experimental scaffold (wheel breathing pattern + polarity),
- a candidate-ranking method only if lift/robustness tests pass.

It does not constitute a proof of RH or a new definition of primes. It is compatible with known modular filtering (wheel factorization) but reinterprets it as a geometric/annotable structure.

---

## 6. Reproducibility checklist
- Fix \(P\), window definitions, and baselines.
- Publish code for \(R(P)\), \(\mathcal{G}(P)\), and candidate extraction.
- Log seeds for random baseline.
- Report lift + variance across windows.

---

## Appendix A — Minimal pseudocode
```pseudo
function residues(P):
  R=[]
  for r in 1..P:
    if gcd(r,P)==1: R.append(r)
  sort(R)
  return R

function breathing_gaps(P):
  R=residues(P)
  G=[]
  for i in 0..len(R)-2: G.append(R[i+1]-R[i])
  G.append(P + R[0] - R[-1])
  return G
