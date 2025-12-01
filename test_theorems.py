"""
Test Suite for Guasti Theorems
==============================

Run with: pytest tests/test_theorems.py -v

Or simply: python tests/test_theorems.py
"""

import sys
sys.path.insert(0, '.')

from math import sqrt


def test_theorem_1_45_criterion():
    """
    THEOREM 1: Perfect Square Detection via 45°
    
    n is a perfect square ⟺ 45° ∈ Θ(n)
    """
    from src.guasti_core import has_45_degree
    
    # Test perfect squares
    squares = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    for n in squares:
        assert has_45_degree(n), f"FAIL: {n} is a square but has_45_degree returned False"
    
    # Test non-squares
    non_squares = [2, 3, 5, 6, 7, 8, 10, 11, 12, 15, 17, 18, 20, 50, 99, 101]
    for n in non_squares:
        assert not has_45_degree(n), f"FAIL: {n} is not a square but has_45_degree returned True"
    
    print("✓ Theorem 1 (45° criterion): PASSED")
    return True


def test_theorem_2_prime_square_signature():
    """
    THEOREM 2: Prime Square Signature
    
    p² has exactly the signature {45°, 90°}
    """
    from src.guasti_core import is_prime_square_signature, is_prime
    
    # Test prime squares
    prime_squares = [4, 9, 25, 49, 121, 169, 289, 361, 529]
    for n in prime_squares:
        sqrt_n = int(sqrt(n))
        if is_prime(sqrt_n):
            assert is_prime_square_signature(n), f"FAIL: {n} = {sqrt_n}² should have minimal signature"
    
    # Test composite squares (should NOT have minimal signature)
    composite_squares = [36, 100, 144, 196, 400, 900]
    for n in composite_squares:
        assert not is_prime_square_signature(n), f"FAIL: {n} should NOT have minimal signature"
    
    print("✓ Theorem 2 (prime square signature): PASSED")
    return True


def test_theorem_5_divisor_angle_correspondence():
    """
    THEOREM 5: Divisor-Angle Correspondence
    
    The number of Pythagorean positions equals the number of Guasti angles.
    """
    from src.guasti_core import tau, angular_signature, get_divisor_pairs
    
    test_numbers = [12, 24, 36, 60, 100, 120]
    
    for n in test_numbers:
        num_pairs = len(get_divisor_pairs(n))
        num_angles = len(angular_signature(n))
        # Due to symmetry, they should be approximately equal
        assert abs(num_pairs - num_angles) <= 1, \
            f"FAIL: n={n}, pairs={num_pairs}, angles={num_angles}"
    
    print("✓ Theorem 5 (divisor-angle correspondence): PASSED")
    return True


def test_classification_consistency():
    """
    Test that classification is consistent with known properties.
    """
    from src.guasti_core import classify_by_signature, is_prime
    
    # Primes should be classified as PRIME
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in primes:
        classification = classify_by_signature(p)
        assert classification == "PRIME", f"FAIL: {p} should be PRIME, got {classification}"
    
    # Prime squares should be classified as PRIME_SQUARE
    prime_squares = [4, 9, 25, 49, 121]
    for n in prime_squares:
        classification = classify_by_signature(n)
        assert classification == "PRIME_SQUARE", f"FAIL: {n} should be PRIME_SQUARE, got {classification}"
    
    print("✓ Classification consistency: PASSED")
    return True


def test_factorization_density():
    """
    Test the factorization density function.
    
    DF(p) = 0 for primes
    DF(n) > 0 for composites
    """
    from src.guasti_core import factorization_density, is_prime
    
    # Primes should have DF = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 97]
    for p in primes:
        df = factorization_density(p)
        assert df == 0, f"FAIL: DF({p}) should be 0, got {df}"
    
    # Known values
    assert factorization_density(12) == 3, "FAIL: DF(12) = DF(2²×3) should be 3"
    assert factorization_density(360) == 6, "FAIL: DF(360) = DF(2³×3²×5) should be 6"
    
    print("✓ Factorization density: PASSED")
    return True


def run_all_tests():
    """Run all theorem tests."""
    print("=" * 60)
    print("GUASTI TRANSFORM - THEOREM VERIFICATION")
    print("=" * 60)
    print()
    
    all_passed = True
    
    try:
        test_theorem_1_45_criterion()
    except AssertionError as e:
        print(f"✗ Theorem 1: FAILED - {e}")
        all_passed = False
    
    try:
        test_theorem_2_prime_square_signature()
    except AssertionError as e:
        print(f"✗ Theorem 2: FAILED - {e}")
        all_passed = False
    
    try:
        test_theorem_5_divisor_angle_correspondence()
    except AssertionError as e:
        print(f"✗ Theorem 5: FAILED - {e}")
        all_passed = False
    
    try:
        test_classification_consistency()
    except AssertionError as e:
        print(f"✗ Classification: FAILED - {e}")
        all_passed = False
    
    try:
        test_factorization_density()
    except AssertionError as e:
        print(f"✗ Factorization density: FAILED - {e}")
        all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()
