Key = tuple[int, int]

class RSA:
    @staticmethod
    def _encrypt(key: Key, message: bytes | bytearray) -> bytes:
        n, e = key

        return 
