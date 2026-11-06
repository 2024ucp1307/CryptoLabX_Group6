
import secrets
import time
from pathlib import Path
from sympy import isprime

BIT_LENGTH = 512
ROUNDS = 20


def mod_pow(base, exponent, modulus):
    result = 1
    base %= modulus

    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus

        exponent >>= 1
        base = (base * base) % modulus

    return result


def miller_rabin(n, rounds):
    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = mod_pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = (x * x) % n

            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime():
    candidates = 0

    while True:
        candidates += 1

        # Generate an exact 512-bit odd integer
        n = secrets.randbits(BIT_LENGTH)
        n |= (1 << (BIT_LENGTH - 1))
        n |= 1

        if miller_rabin(n, ROUNDS):
            return n, candidates


def main():
    print("MILLER-RABIN PRIME GENERATION")
    print("=" * 45)

    start = time.perf_counter()

    prime, candidates = generate_prime()

    # Independent verification using SymPy
    verified = isprime(prime)

    end = time.perf_counter()
    elapsed = end - start

    actual_bits = prime.bit_length()

    print("\nEXPERIMENTAL RESULTS")
    print("-" * 45)

    print("Assigned bit length:", BIT_LENGTH)
    print("Generated prime (hex):")
    print(hex(prime))
    print("Actual bit length:", actual_bits)
    print("Candidates tested:", candidates)
    print("Miller-Rabin rounds:", ROUNDS)
    print(f"Execution time: {elapsed:.6f} seconds")

    print("\nVERIFICATION")
    print("-" * 45)

    print("Bit length verification:",
          "PASSED" if actual_bits == BIT_LENGTH else "FAILED")

    print("Miller-Rabin verification: PASSED")
    print("Independent SymPy verification:",
          "PASSED" if verified else "FAILED")

    if actual_bits != BIT_LENGTH or not verified:
        raise RuntimeError("Prime verification failed!")

    # Save experimental results
    output_dir = Path(__file__).resolve().parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "results.txt"

    with open(output_file, "w") as f:
        f.write("MILLER-RABIN PRIME GENERATION\n")
        f.write("=" * 45 + "\n")
        f.write(f"Assigned bit length: {BIT_LENGTH}\n")
        f.write(f"Generated prime (hex): {hex(prime)}\n")
        f.write(f"Actual bit length: {actual_bits}\n")
        f.write(f"Candidates tested: {candidates}\n")
        f.write(f"Miller-Rabin rounds: {ROUNDS}\n")
        f.write(f"Execution time: {elapsed:.6f} seconds\n")
        f.write("\nVERIFICATION\n")
        f.write("Bit length verification: PASSED\n")
        f.write("Miller-Rabin verification: PASSED\n")
        f.write("Independent SymPy verification: PASSED\n")

    print("\nResults saved to outputs/results.txt")


if __name__ == "__main__":
    main()
