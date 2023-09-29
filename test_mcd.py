# Import your gcd function
from ops import gcd


# Test case 1: gcd of two prime numbers should be 1
def test_gcd_prime_numbers():
    assert gcd(7, 11) == 1


# Test case 2: gcd of two identical numbers should be the number itself
def test_gcd_identical_numbers():
    assert gcd(8, 8) == 8


# Test case 3: gcd of a number and 0 should be the number itself
def test_gcd_with_zero():
    assert gcd(10, 0) == 10


# Test case 4: gcd of two even numbers should be the smaller number
def test_gcd_even_numbers():
    assert gcd(16, 20) == 4


# Test case 5: gcd of two numbers with a common divisor
def test_gcd_common_divisor():
    assert gcd(36, 48) == 12


# Test case 6: gcd of two numbers with no common divisor other than 1
def test_gcd_no_common_divisor():
    assert gcd(17, 19) == 1


# Test case 7: gcd of zero and zero should be zero
def test_gcd_both_zeros():
    assert gcd(0, 0) == 0


# Test case 8: gcd of a large number and a small number
def test_gcd_large_small_numbers():
    assert gcd(987654321, 12345) == 3


# Test case 9: gcd of two large prime numbers
def test_gcd_large_prime_numbers():
    assert gcd(999999937, 999999929) == 1


# Test case 10: gcd of two large numbers with a common divisor
def test_gcd_large_numbers_common_divisor():
    assert gcd(1234567890, 987654321) == 9


# Test case 11: gcd of two very large numbers (stress test)
def test_gcd_very_large_numbers():
    assert (
        gcd(123456789012345678901234567890, 98765432109876543210987654321)
        == 900000000090000000009
    )


# Test case 12: gcd of two very large identical numbers (stress test)
def test_gcd_very_large_identical_numbers():
    assert (
        gcd(999999999999999999999999999999, 999999999999999999999999999999)
        == 999999999999999999999999999999
    )


# Test case 13: gcd of two very large prime numbers (stress test)
def test_gcd_very_large_prime_numbers():
    assert gcd(999999999989, 999999999979) == 1


# Test case 14: gcd of two very large numbers with a common divisor (stress test)
def test_gcd_very_large_numbers_common_divisor():
    assert gcd(999999999990, 999999999980) == 10


# Test case 15: gcd of two very large random numbers (stress test)
def test_gcd_very_large_random_numbers():
    assert gcd(987654321234567890, 1234567890987654321) == 1


# Test case 16: gcd of a large number and zero
def test_gcd_large_number_and_zero():
    assert gcd(1234567890, 0) == 1234567890


# Test case 17: gcd of zero and a large number
def test_gcd_zero_and_large_number():
    assert gcd(0, 1234567890) == 1234567890


# Test case 18: gcd of two very large numbers with no common divisor other than 1 (stress test)
def test_gcd_very_large_no_common_divisor():
    assert gcd(999999999989, 999999999991) == 1


# Test case 19: gcd of a large prime number and zero
def test_gcd_large_prime_number_and_zero():
    assert gcd(999999937, 0) == 999999937


# Test case 20: gcd of zero and a large prime number
def test_gcd_zero_and_large_prime_number():
    assert gcd(0, 999999937) == 999999937


# Test case 21: gcd of a very large prime number and one
def test_gcd_large_prime_number_and_one():
    assert gcd(999999937, 1) == 1


# Test case 22: gcd of one and a very large prime number
def test_gcd_one_and_large_prime_number():
    assert gcd(1, 999999937) == 1
