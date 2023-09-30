from typing import Any, Callable
from typing_extensions import override
from ops import gcd, is_prime, mod_exp, gcde, randbits
from dataclasses import dataclass

import hashlib

Key = tuple[int, int]


@dataclass(frozen=True)
class Keys:
    public: Key
    private: Key


class RSA:
    key_len: int
    keys: Keys

    def __init__(self, key_len: int, e: int, p: int = -1, q: int = -1) -> None:
        self.key_len = key_len
        self.keys = RSA.generate(key_len, e, p, q)

    def encrypt(self, message: int) -> int:
        return self.apply(self.keys.public, message)

    def decrypt(self, ciphertext: int) -> int:
        return self.apply(self.keys.private, ciphertext)

    @staticmethod
    def apply(key: Key, value: int) -> int:
        return mod_exp(value, *reversed(key))

    @staticmethod
    def generate(key_len: int, e: int, p: int = -1, q: int = -1) -> Keys:
        if p < 0 or q < 0:
            p = RSA.gen_prime(key_len // 2, e, {e})
            q = RSA.gen_prime(key_len // 2, e, {e, p})

        n = p * q
        euler = (p - 1) * (q - 1)
        gcd, e_inv, _ = gcde(e, euler)
        d = (e_inv + euler) if e_inv < 0 else (e_inv % euler)

        assert gcd == 1
        assert (e * d) % euler == 1

        return Keys(public=(n, e), private=(n, d))

    @staticmethod
    def gen_prime(bits: int, e: int, exclude: set[int] = set()) -> int:
        while True:
            n = randbits(bits) | 1

            if n > 1 and n not in exclude and is_prime(n) and gcd(e, n - 1) == 1:
                return n


class RSAOAEP(RSA):
    def __init__(self, key_len: int, e: int, p: int = -1, q: int = -1) -> None:
        super().__init__(key_len, e, p, q)

    @override
    def encrypt(self, message: bytes | bytearray, hash: bytes | bytearray, seed: bytes | bytearray, hash_function = hashlib.sha1) -> bytes: # type: ignore[override]
        t, h = self.key_len // 8, len(hash)
        zero_padding = (t - 2 * h - 2) - len(message)
        z_len = t - h - 1
        assert len(hash) == len(seed)
        assert zero_padding >= 0

        partial_pad = hash + (b"\x00" * zero_padding) + b"\x01" + message
        seed_mask = RSAOAEP.mask_gen(seed, z_len, hash_function)

        assert len(partial_pad) == len(seed_mask)

        z = int.from_bytes(seed_mask) ^ int.from_bytes(partial_pad)
        z_prime = z.to_bytes(z_len, "big")
        z_prime_mask = RSAOAEP.mask_gen(z_prime, h, hash_function)
        r2 = int.from_bytes(seed) ^ int.from_bytes(z_prime_mask)
        r_prime = r2.to_bytes(h, "big")
        padded = b"\x00" + r_prime + z_prime

        assert len(padded) == t

        ciphertext = super().encrypt(int.from_bytes(padded))

        return ciphertext.to_bytes(t, "big")

    @override
    def decrypt(self, ciphertext: bytes | bytearray, h: int, message_len: int, hash_function = hashlib.sha1) -> bytes: # type: ignore[override]
        t = self.key_len // 8
        z_len = t - h - 1
        y = int.from_bytes(ciphertext, "big")
        x = super().decrypt(y).to_bytes(t, "big")

        r_prime, z_prime = x[1: 1 + h], x[1 + h:]
        z_mask = RSAOAEP.mask_gen(z_prime, h, hash_function)
        seed = int.from_bytes(z_mask, "big") ^ int.from_bytes(r_prime)
        r_mask = RSAOAEP.mask_gen(seed.to_bytes(h), z_len, hash_function)
        z = int.from_bytes(r_mask) ^ int.from_bytes(z_prime)

        return z.to_bytes(z_len, "big")[-message_len:]

    @staticmethod
    def mask_gen(seed: bytes | bytearray, mask_len: int, hash_function = hashlib.sha1) -> bytes:
        hash_len: int = hash_function().digest_size
        assert mask_len <= (hash_len << 32)

        counter = 0
        mask = bytearray()

        while len(mask) < mask_len:
            counter_bytes = counter.to_bytes(4, "big")
            hash = hash_function(seed + counter_bytes).digest()
            mask.extend(hash)
            counter += 1

        return mask[:mask_len]
