import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# =====================================================================
# SETUP: Ciphertext, IV, and Padding Oracle Function
# (Note: The secret key is hidden and NEVER accessed by the attack code)
# =====================================================================
_SECRET_KEY = os.urandom(16)  # 128-bit secret AES key
BLOCK_SIZE = 16

def create_sample_ciphertext():
    """Generates a sample ciphertext for demonstration."""
    secret_message = b"Padding Oracle Attacks are extremely powerful!"
    iv = os.urandom(BLOCK_SIZE)
    cipher = AES.new(_SECRET_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(secret_message, BLOCK_SIZE))
    return iv, ciphertext

# Generate IV and Ciphertext for testing
IV, CIPHERTEXT = create_sample_ciphertext()

# Global query counter for Task 3
oracle_query_count = 0

def padding_oracle(iv: bytes, ciphertext: bytes) -> bool:
    """
    Padding Oracle Function:
    Returns True if the decrypted ciphertext has valid PKCS#7 padding.
    Returns False otherwise.
    """
    global oracle_query_count
    oracle_query_count += 1
    
    try:
        cipher = AES.new(_SECRET_KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        unpad(decrypted, BLOCK_SIZE, style='pkcs7')
        return True
    except (ValueError, KeyError):
        return False

# =====================================================================
# TASK 2: ATTACK IMPLEMENTATION
# =====================================================================

def attack_block(prev_block: bytes, target_block: bytes) -> bytes:
    """
    Recovers the intermediate state bytes I_i for a target block
    by modifying the previous block (or IV) from right to left.
    """
    intermediate_block = bytearray(BLOCK_SIZE)
    c_prime = bytearray(prev_block)
    
    # Process bytes from right to left (index 15 down to 0)
    for byte_idx in range(BLOCK_SIZE - 1, -1, -1):
        target_padding = BLOCK_SIZE - byte_idx
        
        # Prepare c_prime bytes on the right (indices > byte_idx)
        # so that when decrypted, they yield the target_padding value
        for right_idx in range(byte_idx + 1, BLOCK_SIZE):
            c_prime[right_idx] = intermediate_block[right_idx] ^ target_padding
            
        found_byte = False
        # Try all 256 possible byte values for c_prime[byte_idx]
        for guess in range(256):
            c_prime[byte_idx] = guess
            
            # Query padding oracle with modified prev_block and target_block
            if padding_oracle(bytes(c_prime), target_block):
                # Handle edge case for target_padding = 1 where original padding 
                # might accidentally produce valid multi-byte padding
                if target_padding == 1 and byte_idx > 0:
                    # Check by altering the byte to the left
                    check_prime = bytearray(c_prime)
                    check_prime[byte_idx - 1] ^= 0xFF
                    if not padding_oracle(bytes(check_prime), target_block):
                        continue  # False positive due to existing padding
                
                # Recover intermediate byte I[byte_idx]
                intermediate_block[byte_idx] = guess ^ target_padding
                found_byte = True
                break
                
        if not found_byte:
            raise Exception(f"Failed to find valid byte at index {byte_idx}")
            
    # Derive plaintext byte array: P_i = I_i XOR C_{i-1}
    plaintext_block = bytes(i ^ c for i, c in zip(intermediate_block, prev_block))
    return plaintext_block


def padding_oracle_attack(iv: bytes, ciphertext: bytes) -> bytes:
    """
    Executes the full padding oracle attack across all blocks.
    """
    blocks = [iv] + [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    recovered_plaintext = b""
    
    # Attack each block starting from the first block
    for i in range(1, len(blocks)):
        prev_block = blocks[i-1]
        target_block = blocks[i]
        
        print(f"[*] Decrypting block {i}/{len(blocks)-1}...")
        p_block = attack_block(prev_block, target_block)
        recovered_plaintext += p_block
        
    # Unpad the recovered plaintext using standard PKCS#7 rules
    return unpad(recovered_plaintext, BLOCK_SIZE, style='pkcs7')


if __name__ == "__main__":
    print("==================================================")
    print("   Starting AES-CBC Padding Oracle Attack")
    print("==================================================")
    print(f"[+] IV (hex):         {IV.hex()}")
    print(f"[+] Ciphertext (hex): {CIPHERTEXT.hex()}")
    print("--------------------------------------------------")
    
    # Execute attack
    recovered_message = padding_oracle_attack(IV, CIPHERTEXT)
    
    print("--------------------------------------------------")
    print(f"[+] Recovered Plaintext: \"{recovered_message.decode('utf-8')}\"")
    print(f"[+] Total Oracle Queries: {oracle_query_count}")
    print("==================================================")