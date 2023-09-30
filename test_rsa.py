import secrets
from ops import is_prime, randbits
from rsa import RSA, RSAOAEP

import hashlib

def test_gen_prime():
    BITS = 256
    e = 97

    for _ in range(10):
        assert is_prime(RSA.gen_prime(BITS, e))


def test_rsa_key_gen():
    e, p, q = 7, 11, 13
    n = p * q
    rsa = RSA(1, e, p, q)

    assert rsa.keys.public == (n, e)
    assert rsa.keys.private == (n, 103)


def test_rsa_encryption():
    BITS = 512
    e = 257
    rsa = RSA(BITS, e)
    n, e = rsa.keys.public
    n1, d = rsa.keys.private
    message = randbits(BITS) % n

    assert n == n1
    assert e != d

    ciphertext = rsa.encrypt(message)
    decrypted = rsa.decrypt(ciphertext)

    assert message != ciphertext
    assert message == decrypted


def test_mask_gen():
    assert RSAOAEP.mask_gen(b"foo", 3).hex() == "1ac907"
    assert RSAOAEP.mask_gen(b"foo", 5).hex() == "1ac9075cd4"
    assert RSAOAEP.mask_gen(b"bar", 5).hex() == "bc0c655e01"
    assert RSAOAEP.mask_gen(b"bar", 50).hex() == "bc0c655e016bc2931d85a2e675181adcef7f581f76df2739da74faac41627be2f7f415c89e983fd0ce80ced9878641cb4876"
    assert RSAOAEP.mask_gen(b"bar", 50, hashlib.sha256).hex() == "382576a7841021cc28fc4c0948753fb8312090cea942ea4c4e735d10dc724b155f9f6069f289d61daca0cb814502ef04eae1"


def test_rsa_oaep_encryption():
    BITS = 512
    e = 257
    rsa = RSAOAEP(BITS, e)
    t = rsa.key_len // 8
    h = 2
    seed = b"\x00" * h
    hash = bytes(seed)
    message = randbits(rsa.key_len // 2).to_bytes(t // 2)

    ciphertext = rsa.encrypt(message, seed, hash)
    decrypted = rsa.decrypt(ciphertext, h, len(message))

    assert message != ciphertext
    assert len(message) == len(decrypted)
    assert message == decrypted
