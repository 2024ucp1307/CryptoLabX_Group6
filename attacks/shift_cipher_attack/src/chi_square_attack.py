import string
from shift_cipher import ShiftCipher

ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074
}

class ChiSquareAttack:
    def solve(self, ciphertext: str) -> int:
        best_key = 0
        min_chi = float('inf')
        
        letters_only = [c.upper() for c in ciphertext if c.isalpha()]
        total_letters = len(letters_only)
        
        if total_letters == 0:
            return 0

        for key in range(26):
            decrypted = ShiftCipher.decrypt("".join(letters_only), key)
            counts = {char: 0 for char in string.ascii_uppercase}
            
            for char in decrypted:
                counts[char] += 1
                
            chi_square = 0.0
            for char in string.ascii_uppercase:
                observed = counts[char]
                expected = total_letters * ENGLISH_FREQ[char]
                chi_square += ((observed - expected) ** 2) / expected
                
            if chi_square < min_chi:
                min_chi = chi_square
                best_key = key
                
        return best_key