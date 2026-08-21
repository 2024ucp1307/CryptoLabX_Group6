import string
from shift_cipher import ShiftCipher

class DictionaryAttack:
    def __init__(self, dictionary_path: str):
        with open(dictionary_path, 'r', encoding='utf-8') as f:
            self.dictionary = set(word.strip().lower() for word in f if word.strip())

    def solve(self, ciphertext: str):
        best_key = 0
        max_matches = -1
        
        for key in range(26):
            decrypted = ShiftCipher.decrypt(ciphertext, key)
            words = decrypted.translate(str.maketrans('', '', string.punctuation)).lower().split()
            matches = sum(1 for word in words if word in self.dictionary)
            
            if matches > max_matches:
                max_matches = matches
                best_key = key
                
        return best_key