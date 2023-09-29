from ops import is_prime
from rsa import RSA

def test_gen_prime():
    BITS = 256
    seed = 97

    for _ in range(10):
        assert is_prime(RSA.gen_prime(BITS, seed))
