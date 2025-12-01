#!/usr/bin/env python3
"""
Basic Usage Example
===================

This script demonstrates the basic functionality of the Guasti Transform.

Run with:
    python examples/basic_usage.py
"""

import sys
sys.path.insert(0, '.')

from src.guasti_core import (
    angular_signature,
    has_45_degree,
    classify_by_signature,
    is_prime,
    tau,
    multiplicative_entropy,
    verify_theorems
)


def main():
    print("=" * 60)
    print("GUASTI TRANSFORM - BASIC USAGE EXAMPLE")
    print("=" * 60)
    
    # Example 1: Perfect Square Detection
    print("\n📐 EXAMPLE 1: Perfect Square Detection (Theorem 1)")
    print("-" * 50)
    
    test_numbers = [25, 26, 36, 37, 49, 50, 100, 101]
    
    for n in test_numbers:
        is_square = has_45_degree(n)
        status = "✓ SQUARE" if is_square else "✗ not square"
        print(f"  n = {n:4d}: {status}")
    
    # Example 2: Prime Square Signature
    print("\n🔷 EXAMPLE 2: Prime Square Signature (Theorem 2)")
    print("-" * 50)
    
    prime_squares = [4, 9, 25, 49, 121]
    composite_squares = [36, 100, 144]
    
    print("Prime squares (p²):")
    for n in prime_squares:
        sig = angular_signature(n)
        print(f"  {n} = {int(n**0.5)}²: signature = {sig}")
    
    print("\nComposite squares:")
    for n in composite_squares:
        sig = angular_signature(n)
        print(f"  {n} = {int(n**0.5)}²: signature has {len(sig)} angles")
    
    # Example 3: Classification
    print("\n📊 EXAMPLE 3: Number Classification")
    print("-" * 50)
    
    all_types = [17, 25, 36, 60]
    
    for n in all_types:
        classification = classify_by_signature(n)
        entropy = multiplicative_entropy(n)
        print(f"  n = {n:3d}: {classification:16s} (H = {entropy:.3f})")
    
    # Example 4: Verify Theorems
    print("\n✅ EXAMPLE 4: Theorem Verification")
    print("-" * 50)
    
    results = verify_theorems(200)
    for theorem, passed in results.items():
        status = "✓ VERIFIED" if passed else "✗ FAILED"
        print(f"  {theorem}: {status}")
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("See the documentation for more advanced usage.")
    print("=" * 60)


if __name__ == "__main__":
    main()
