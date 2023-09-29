from ops import gcd, is_prime, mod_exp, gcde
from dataclasses import dataclass

import secrets

Key = tuple[int, int]

@dataclass(frozen=True)
class Keys:
    public: Key
    private: Key


class RSA:
    keys: Keys

    @staticmethod
    def apply(key: Key, value: int) -> int:
        return mod_exp(value, *reversed(key))

    @staticmethod
    def generate(length: int, seed: int, p: int = -1, q: int = -1) -> Keys:
        if p < 0 or q < 0:
            p = RSA.gen_prime(length, seed)
            q = RSA.gen_prime(length, seed)

        n = p * q
        n2 = (p - 1) * (q - 1) 
        d = gcde(seed, n2)[1] * n2

        return Keys(public=(n, seed), private=(n, d))

    @staticmethod
    def gen_prime(length: int, seed: int) -> int:
        while True:
            n = secrets.randbits(length) | 1

            if n > 1 and is_prime(n) and gcd(seed, n - 1) == 1:
                return n

