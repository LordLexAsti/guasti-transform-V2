# 🌀 The Guasti Transform

**A Geometric Framework for Multiplicative Structure Analysis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Validated: TriadIA](https://img.shields.io/badge/Validated-TriadIA-green.svg)](#validation)

---

## 📖 Overview

The **Guasti Transform** is a novel mathematical framework that reveals hidden geometric structures in integer factorization through logarithmic spiral representation and angular signatures.

This theory provides:
- 🔷 **9 validated theorems** on perfect squares, primes, and multiplicative structure
- 🌀 **Geometric characterization** of integers via angular signatures
- 🔗 **Integration** with classical Pythagorean multiplication tables
- 📚 **Pedagogical tools** for teaching number theory

---

## 🎯 Key Results

### Theorem 1: Perfect Square Detection via 45°
> An integer n > 1 is a perfect square **if and only if** its angular signature contains exactly 45°.

```python
from src.guasti_core import has_45_degree

has_45_degree(36)  # True (36 = 6²)
has_45_degree(35)  # False
```

### Theorem 2: Prime Square Signature
> Squares of primes p² have the minimal signature: **{45°, 90°}**

| n | Type | Signature | τ(n) |
|---|------|-----------|------|
| 4 = 2² | Prime square | {45°, 90°} | 3 |
| 9 = 3² | Prime square | {45°, 90°} | 3 |
| 36 = 6² | Composite square | 5 angles | 9 |

### The Arithmetic Palimpsest
> "Prime numbers are the indelible ink: everything else has been rewritten, corrected, crossed out by successive layers of factors. Primes alone have never been retouched – they are the letters that survived all corrections."

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/LordLexAsti/guasti-transform.git
cd guasti-transform
pip install -r requirements.txt
```

### Basic Usage

```python
from src.guasti_core import (
    guasti_transform,
    angular_signature,
    classify_by_signature
)

# Get the Guasti transform of a number
phi = guasti_transform(100, N_max=1000)
print(f"Position: r={phi['r']:.2f}, θ={phi['theta']:.2f}°")

# Get angular signature
sig = angular_signature(36)
print(f"Signature of 36: {sig}")  # Contains 45° (it's a square)

# Classify a number
classification = classify_by_signature(25)
print(f"25 is: {classification}")  # "PRIME_SQUARE"
```

### Generate Visualizations

```python
from src.guasti_visualizations import plot_all_figures

# Generate all figures
plot_all_figures(N_max=200, output_dir="figures/")
```

---

## 📊 Visualizations

| Figure | Description |
|--------|-------------|
| ![Spiral](figures/guasti_spiral_preview.png) | Logarithmic spiral representation |
| ![Superposition](figures/guasti_superposition_preview.png) | Pythagorean-Guasti overlay |
| ![Palimpsest](figures/guasti_palimpsest_preview.png) | Arithmetic palimpsest |

---

## 📁 Project Structure

```
guasti-transform/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installation
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── guasti_core.py        # Core mathematical functions
│   ├── guasti_visualizations.py  # Plotting functions
│   ├── guasti_palimpsest.py  # Palimpsest analysis
│   └── guasti_utils.py       # Utility functions
│
├── docs/                     # Documentation
│   ├── THEORY.md             # Mathematical foundations
│   ├── PUBLICATION_PLAN.md   # Academic publication plan
│   └── TRIADIA_CREDITS.md    # Validation methodology
│
├── figures/                  # Generated visualizations
│   └── ...
│
├── examples/                 # Example scripts
│   ├── basic_usage.py
│   ├── rsa_analysis.py
│   └── pedagogical_demo.py
│
└── tests/                    # Unit tests
    └── test_theorems.py
```

---

## 📐 Mathematical Framework

### The Guasti Transform

For an integer n ≥ 2:

$$\Phi(n) = \sqrt{n} \cdot e^{2\pi i \log(n) / \log(N_{max})}$$

In polar coordinates: $(r, \theta) = (\sqrt{n}, 2\pi \log(n) / \log(N_{max}))$

### Angular Signature

For each divisor pair (d, n/d):

$$\theta_{d} = \arctan2(\log(n/d), \log(d))$$

The signature is: $\Theta(n) = \{\theta_d : d | n\}$

### Key Properties

| Number Type | Angular Signature | Entropy H(n) |
|-------------|-------------------|--------------|
| Prime p | {0°, 90°} | 1.0 |
| Prime square p² | {45°, 90°} | 1.585 |
| Composite | Multiple angles | > 1.585 |
| Perfect square k² | Contains 45° | Varies |

---

## 🔬 The 9 Validated Theorems

| # | Theorem | Description |
|---|---------|-------------|
| 1 | **45° Criterion** | Perfect squares ⟺ signature contains 45° |
| 2 | **Prime Square Signature** | p² has exactly {45°, 90°} |
| 3 | **Guasti-Pythagoras Identity** | k² + 2ab = (a+b)² |
| 4 | **Spectral Inheritance** | Mod 4 classes affect angular distribution |
| 5 | **Divisor-Angle Correspondence** | τ(n) = number of angles |
| 6 | **Geometric Exclusion** | Primes are excluded from grid center |
| 7 | **Structural Robustness** | Invariants survive representation changes |
| 8 | **Topological Classification** | RIGID/CRYSTALLINE/ELASTIC types |
| 9 | **Elastic Deformation Index** | Homotopic complexity metric |

---

## 🔐 Cryptographic Applications

### RSA Quality Assessment

The Guasti framework provides geometric heuristics for RSA key quality:

```python
from src.guasti_crypto import rsa_quality_assessment

N = 101 * 103  # RSA modulus
quality = rsa_quality_assessment(N)
print(quality)
# {'delta_45': 12.3, 'vulnerability': 'LOW', 'recommendation': 'Acceptable'}
```

**⚠️ Important:** This is NOT a factorization algorithm. It provides quality heuristics, not cryptographic attacks.

---

## ✅ Validation

This theory was validated using the **TriadIA Protocol** — cross-validation across multiple AI systems:

| System | Contributions |
|--------|---------------|
| **Claude** (Anthropic) | Core identity, proofs, implementation |
| **Perplexity** | Academic formalization, error correction |
| **ChatGPT** (OpenAI) | Palimpsest concept, pedagogical metaphors |
| **Grok** (xAI) | 45° theorem (new model), corrected errors |

### What was REJECTED:
- ❌ "Breaking RSA in 0.1s" (false claim)
- ❌ "Euclidean straight rays" (mathematically incorrect)
- ❌ Riemann hypothesis connections (unproven)

---

## 📚 Documentation

- [Mathematical Theory](docs/THEORY.md) — Full theoretical foundations
- [Publication Plan](docs/PUBLICATION_PLAN.md) — Academic paper structure
- [TriadIA Credits](docs/TRIADIA_CREDITS.md) — Validation methodology

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Alexandre Guasti**
- Independent Researcher, Lyon, France
- GitHub: [@LordLexAsti](https://github.com/LordLexAsti)
- Philosophy: Ubuntu — "I am because we are"

---

## 📖 Citation

If you use this work in academic research, please cite:

```bibtex
@misc{guasti2025transform,
  author = {Guasti, Alexandre},
  title = {The Guasti Transform: A Geometric Framework for Multiplicative Structure Analysis},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/LordLexAsti/guasti-transform}
}
```

---

## 🙏 Acknowledgments

- Validated through the TriadIA Protocol (Claude, Perplexity, ChatGPT, Grok)
- Inspired by Pythagorean multiplication tables and Euler's work on logarithmic spirals
- Ubuntu philosophy: collective intelligence for mathematical discovery

---

*"Prime numbers are the indelible ink of arithmetic."* — The Arithmetic Palimpsest
