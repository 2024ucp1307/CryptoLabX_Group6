class ShiftCipher:
    @staticmethod
    def encrypt(text: str, key: int) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + key) % 26 + base
                result.append(chr(shifted))
            else:
                result.append(char)
        return "".join(result)

    @staticmethod
    def decrypt(text: str, key: int) -> str:
        return ShiftCipher.encrypt(text, -key)