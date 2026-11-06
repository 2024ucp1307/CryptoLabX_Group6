
import random
import secrets
import string
import time
from pathlib import Path

KNOWN_TEXT = "A" * 14
SEED_SPACE = 65536
TOKEN_SIZE = 16
TIME_WINDOW = 300


# Generate MT19937 keystream
def generate_keystream(seed, length):
    rng = random.Random(seed)
    return bytes(rng.getrandbits(8) for _ in range(length))


# XOR encryption and decryption
def encrypt_decrypt(data, seed):
    keystream = generate_keystream(seed, len(data))
    return bytes(a ^ b for a, b in zip(data, keystream))


# Generate random printable prefix
def generate_prefix():
    length = secrets.randbelow(16) + 5
    return ''.join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )


# PART A: MT19937 STREAM CIPHER
def part_a():
    print("\n========== PART A: MT19937 STREAM CIPHER ==========")

    # Encryption and decryption demonstration
    message = b"Hello MT19937 Stream Cipher"
    seed = secrets.randbelow(SEED_SPACE)

    ciphertext = encrypt_decrypt(message, seed)
    decrypted = encrypt_decrypt(ciphertext, seed)

    print("\nEncryption/Decryption Demonstration")
    print("Original message :", message.decode())
    print("Seed             :", seed)
    print("Ciphertext (hex) :", ciphertext.hex())
    print("Decrypted message:", decrypted.decode())
    print("Verification     :", decrypted == message)

    # Generate challenge plaintext
    prefix = generate_prefix()
    plaintext = (prefix + KNOWN_TEXT).encode()
    secret_seed = secrets.randbelow(SEED_SPACE)

    ciphertext = encrypt_decrypt(plaintext, secret_seed)

    print("\nKnown Plaintext Attack")
    print("Plaintext        :", plaintext.decode())
    print("Ciphertext (hex) :", ciphertext.hex())
    print("Known text       :", KNOWN_TEXT)
    print("Original seed    :", secret_seed)

    # Brute-force all 16-bit seeds
    print("\nBrute Force Seed Recovery")

    recovered = None
    recovered_plaintext = None
    candidates = 0

    for candidate in range(SEED_SPACE):
        candidates += 1

        decrypted_text = encrypt_decrypt(ciphertext, candidate)

        if KNOWN_TEXT.encode() in decrypted_text:
            recovered = candidate
            recovered_plaintext = decrypted_text
            break

    print("Seed space       :", SEED_SPACE)
    print("Candidates tested:", candidates)

    if recovered is None:
        print("Seed recovery failed")
        return {
            "candidates": candidates,
            "verified": False
        }

    # A successful seed recovery always assigns the matching plaintext.
    assert recovered_plaintext is not None

    print("Recovered seed   :", recovered)
    print("Recovered text   :", recovered_plaintext.decode())
    
    full_check = (
        encrypt_decrypt(ciphertext, recovered) == plaintext
    )

    print("\nPart A Verification")
    print("Seed recovered correctly:", recovered == secret_seed)
    print("Full plaintext recovered:", full_check)
    print("Known text found        :",
          KNOWN_TEXT.encode() in recovered_plaintext)

    return {
        "candidates": candidates,
        "plaintext": plaintext.decode(),
        "ciphertext": ciphertext.hex(),
        "original_seed": secret_seed,
        "recovered_seed": recovered,
        "verified": full_check
    }


# PART B: TIMESTAMP-BASED RESET TOKEN
def generate_token(timestamp):
    return generate_keystream(timestamp, TOKEN_SIZE)


def part_b():
    print("\n========== PART B: RESET TOKEN ATTACK ==========")

    # Generate token using current Unix timestamp
    timestamp = int(time.time())

    token = generate_token(timestamp)

    print("\nToken Generation")
    print("Timestamp       :", timestamp)
    print("Generated token:", token.hex())
    print("Token size      :", len(token), "bytes")

    # Search timestamp range
    start_time = max(0, timestamp - TIME_WINDOW)
    end_time = timestamp + TIME_WINDOW

    print("\nTimestamp Brute Force")
    print("Search start:", start_time)
    print("Search end  :", end_time)

    candidates = 0
    recovered_timestamp = None

    for candidate in range(start_time, end_time + 1):
        candidates += 1

        candidate_token = generate_token(candidate)

        if candidate_token == token:
            recovered_timestamp = candidate
            break

    print("Timestamps tested:", candidates)

    if recovered_timestamp is None:
        print("Timestamp recovery failed")
        return {
            "timestamp": timestamp,
            "token": token.hex(),
            "candidates": candidates,
            "verified": False
        }

    # Verify recovered timestamp
    regenerated_token = generate_token(recovered_timestamp)

    verified = regenerated_token == token

    print("Recovered timestamp:", recovered_timestamp)
    print("Regenerated token  :", regenerated_token.hex())
    print("Token verification :", verified)

    return {
        "timestamp": timestamp,
        "recovered_timestamp": recovered_timestamp,
        "token": token.hex(),
        "candidates": candidates,
        "verified": verified,
        "start": start_time,
        "end": end_time
    }


# SAVE EXPERIMENTAL RESULTS
def save_results(a, b):
    output_path = (
        Path(__file__).resolve().parent.parent
        / "outputs"
        / "results.txt"
    )

    with open(output_path, "w") as file:

        file.write("MT19937 STREAM CIPHER AND TOKEN ATTACK\n")
        file.write("=" * 50 + "\n\n")

        file.write("PART A: STREAM CIPHER\n")
        file.write("-" * 40 + "\n")

        for key, value in a.items():
            file.write(f"{key}: {value}\n")

        file.write("\nPART B: TIMESTAMP TOKEN ATTACK\n")
        file.write("-" * 40 + "\n")

        for key, value in b.items():
            file.write(f"{key}: {value}\n")

    print("\nResults saved to:", output_path)


# MAIN FUNCTION
def main():
    start = time.time()

    result_a = part_a()
    result_b = part_b()

    save_results(result_a, result_b)

    print("\n========== ASSIGNMENT COMPLETED ==========")
    print("Execution time:", round(time.time() - start, 4), "seconds")


if __name__ == "__main__":
    main()
