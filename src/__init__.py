"""
Guasti Transform Package
========================

A geometric framework for multiplicative structure analysis.

Main modules:
- guasti_core: Core mathematical functions
- guasti_visualizations: Plotting and visualization
- guasti_palimpsest: Palimpsest analysis
- guasti_utils: Utility functions

Quick Start:
    >>> from src.guasti_core import angular_signature, has_45_degree
    >>> sig = angular_signature(36)
    >>> has_45_degree(36)  # True - it's a perfect square
"""

from .guasti_core import (
    guasti_transform,
    angular_signature,
    has_45_degree,
    is_prime_square_signature,
    classify_by_signature,
    tau,
    sigma,
    is_prime,
    get_divisor_pairs,
)

__version__ = "2.0.0"
__author__ = "Alexandre Guasti"
__email__ = ""
__license__ = "MIT"

__all__ = [
    "guasti_transform",
    "angular_signature",
    "has_45_degree",
    "is_prime_square_signature",
    "classify_by_signature",
    "tau",
    "sigma",
    "is_prime",
    "get_divisor_pairs",
]
