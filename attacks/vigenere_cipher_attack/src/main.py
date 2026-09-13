from collections import defaultdict
import os


ENGLISH_FREQUENCY = [
    0.082, 0.015, 0.028, 0.043, 0.127, 0.022,
    0.020, 0.061, 0.070, 0.0015, 0.0077, 0.040,
    0.024, 0.067, 0.075, 0.019, 0.001,
    0.060, 0.063, 0.091, 0.028, 0.0098,
    0.024, 0.0015, 0.020, 0.00074
]


def clean_ciphertext(ciphertext):
    result = ""

    for char in ciphertext:
        if 'a' <= char <= 'z':
            char = chr(ord(char) - 32)

        if 'A' <= char <= 'Z':
            result += char

    return result


def find_repeated_patterns(ciphertext):
    patterns = defaultdict(list)

    for length in range(3, 6):
        for i in range(len(ciphertext) - length + 1):
            pattern = ciphertext[i:i + length]
            patterns[pattern].append(i)

    repeated_patterns = {}

    for pattern, positions in patterns.items():
        if len(positions) >= 2:
            repeated_patterns[pattern] = positions

    return repeated_patterns


def calculate_distances(patterns):
    distances = []

    for pattern in patterns:
        positions = patterns[pattern]

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                distance = positions[j] - positions[i]
                distances.append(distance)

    return distances


def find_factors(number):
    factors = []

    for i in range(2, 21):
        if number % i == 0:
            factors.append(i)

    return factors


def kasiski_analysis(distances):
    factor_count = {}

    for distance in distances:
        factors = find_factors(distance)

        for factor in factors:
            if factor not in factor_count:
                factor_count[factor] = 0

            factor_count[factor] += 1

    candidates = []

    for length in factor_count:
        candidates.append(
            (length, factor_count[length])
        )

    candidates.sort(
        key=lambda x: (-x[1], x[0])
    )

    return candidates


def calculate_ic(text):
    n = len(text)

    if n <= 1:
        return 0.0

    frequency = [0] * 26

    for char in text:
        index = ord(char) - ord('A')
        frequency[index] += 1

    numerator = 0

    for count in frequency:
        numerator += count * (count - 1)

    denominator = n * (n - 1)

    return numerator / denominator


def split_into_groups(ciphertext, key_length):
    groups = []

    for i in range(key_length):
        group = ""

        for j in range(i, len(ciphertext), key_length):
            group += ciphertext[j]

        groups.append(group)

    return groups


def frequency_analysis(group):
    frequency = [0] * 26

    for char in group:
        index = ord(char) - ord('A')
        frequency[index] += 1

    return frequency


def find_shift(group):
    frequency = frequency_analysis(group)

    n = len(group)

    best_shift = 0
    best_chi_square = float('inf')

    for shift in range(26):
        chi_square = 0.0

        for plain_letter in range(26):

            cipher_letter = (
                plain_letter + shift
            ) % 26

            observed = frequency[cipher_letter]

            expected = (
                n * ENGLISH_FREQUENCY[plain_letter]
            )

            if expected > 0:
                difference = observed - expected

                chi_square += (
                    difference * difference
                ) / expected

        if chi_square < best_chi_square:
            best_chi_square = chi_square
            best_shift = shift

    return best_shift


def calculate_average_ic(ciphertext, key_length):
    groups = split_into_groups(
        ciphertext,
        key_length
    )

    total_ic = 0.0

    for group in groups:
        total_ic += calculate_ic(group)

    return total_ic / key_length


def estimate_key_length(ciphertext, kasiski_candidates):
    candidate_lengths = []

    for length, count in kasiski_candidates:
        if 2 <= length <= 20:
            candidate_lengths.append(length)

    for length in range(2, 21):
        if length not in candidate_lengths:
            candidate_lengths.append(length)

    best_length = 2
    best_ic = -1.0

    for length in candidate_lengths:
        average_ic = calculate_average_ic(
            ciphertext,
            length
        )

        if average_ic > best_ic:
            best_ic = average_ic
            best_length = length

    return best_length


def find_key(groups):
    key = ""

    for group in groups:
        shift = find_shift(group)

        key += chr(
            ord('A') + shift
        )

    return key


def vigenere_decrypt(ciphertext, key):
    plaintext = ""

    for i in range(len(ciphertext)):

        cipher_value = (
            ord(ciphertext[i]) - ord('A')
        )

        key_value = (
            ord(key[i % len(key)]) - ord('A')
        )

        plain_value = (
            cipher_value - key_value
        ) % 26

        plaintext += chr(
            ord('A') + plain_value
        )

    return plaintext


def vigenere_encrypt(plaintext, key):
    ciphertext = ""

    for i in range(len(plaintext)):

        plain_value = (
            ord(plaintext[i]) - ord('A')
        )

        key_value = (
            ord(key[i % len(key)]) - ord('A')
        )

        cipher_value = (
            plain_value + key_value
        ) % 26

        ciphertext += chr(
            ord('A') + cipher_value
        )

    return ciphertext


def verify(plaintext, key, original_ciphertext):
    regenerated = vigenere_encrypt(
        plaintext,
        key
    )

    return regenerated == original_ciphertext


def display_frequency_table(group, group_number):
    frequency = frequency_analysis(group)

    data = []

    for i in range(26):
        data.append(
            (
                chr(ord('A') + i),
                frequency[i]
            )
        )

    data.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print(
        f"\nGROUP {group_number + 1}"
    )

    print("-" * 40)
    print("Letter\tCount\tPercentage")

    for letter, count in data:

        percentage = (
            count / len(group)
        ) * 100

        print(
            f"{letter}\t"
            f"{count}\t"
            f"{percentage:.2f}%"
        )


def load_ciphertext():
    current_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    testcase_directory = os.path.join(
        current_directory,
        "..",
        "testcases"
    )

    filepath = os.path.join(
        testcase_directory,
        "ciphertext.txt"
    )

    with open(filepath, "r") as file:
        ciphertext = file.read()

    return clean_ciphertext(ciphertext)


def display_repeated_patterns(patterns):
    print("\nREPEATED PATTERNS")
    print("-" * 60)

    for pattern, positions in patterns.items():
        print(
            f"{pattern}: "
            + " ".join(
                str(position)
                for position in positions
            )
        )


def display_kasiski_candidates(candidates):
    print(
        "\nKASISKI CANDIDATE KEY LENGTHS"
    )

    print("-" * 40)
    print("Length\tFactor Count")

    for length, count in candidates:
        print(
            f"{length}\t{count}"
        )


def save_results(
    ciphertext,
    plaintext,
    key,
    key_length,
    verification
):
    current_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    output_directory = os.path.join(
        current_directory,
        "..",
        "outputs"
    )

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    filepath = os.path.join(
        output_directory,
        "results.txt"
    )

    with open(filepath, "w") as file:

        file.write(
            "VIGENERE CIPHER CRYPTANALYSIS\n"
        )

        file.write(
            "=" * 70 + "\n"
        )

        file.write(
            "Group Number: 6\n"
        )

        file.write(
            "Ciphertext: Ciphertext-2\n"
        )

        file.write(
            f"Ciphertext Length: "
            f"{len(ciphertext)}\n"
        )

        file.write(
            f"Estimated Key Length: "
            f"{key_length}\n"
        )

        file.write(
            f"Recovered Key: "
            f"{key}\n"
        )

        file.write(
            "\nRecovered Plaintext:\n"
        )

        file.write(
            plaintext
        )

        file.write(
            "\n\nVerification: "
        )

        if verification:
            file.write("SUCCESS\n")
        else:
            file.write("FAILED\n")

    return filepath


def main():

    print("=" * 70)
    print(
        "VIGENERE CIPHER CRYPTANALYSIS"
    )
    print(
        "GROUP 6"
    )
    print(
        "KASISKI EXAMINATION + "
        "FREQUENCY ANALYSIS"
    )
    print("=" * 70)

    ciphertext = load_ciphertext()

    print(
        "\nUsing Ciphertext-2"
    )

    print(
        "Group Number: 6"
    )

    print(
        "Clean Ciphertext Length:",
        len(ciphertext)
    )

    print("\n" + "=" * 70)
    print("1. KASISKI EXAMINATION")
    print("=" * 70)

    repeated_patterns = (
        find_repeated_patterns(
            ciphertext
        )
    )

    display_repeated_patterns(
        repeated_patterns
    )

    distances = calculate_distances(
        repeated_patterns
    )

    print(
        "\nDISTANCES BETWEEN "
        "REPEATED PATTERNS"
    )

    print("-" * 60)

    print(distances)

    candidates = kasiski_analysis(
        distances
    )

    display_kasiski_candidates(
        candidates
    )

    estimated_key_length = (
        estimate_key_length(
            ciphertext,
            candidates
        )
    )

    print(
        "\nEstimated Key Length:",
        estimated_key_length
    )

    print(
        "Average IC:",
        f"{calculate_average_ic(ciphertext, estimated_key_length):.6f}"
    )

    print("\n" + "=" * 70)
    print(
        "2. SPLIT CIPHERTEXT "
        "INTO GROUPS"
    )
    print("=" * 70)

    groups = split_into_groups(
        ciphertext,
        estimated_key_length
    )

    for i, group in enumerate(groups):

        print(
            f"\nGroup {i + 1}: "
            f"{group}"
        )

    print("\n" + "=" * 70)
    print("3. FREQUENCY ANALYSIS")
    print("=" * 70)

    for i, group in enumerate(groups):

        display_frequency_table(
            group,
            i
        )

        shift = find_shift(group)

        print(
            "Probable Shift:",
            shift,
            "->",
            chr(ord('A') + shift)
        )

    print("\n" + "=" * 70)
    print("4. KEY RECOVERY")
    print("=" * 70)

    key = find_key(groups)

    print(
        "\nRecovered Key:",
        key
    )

    print("\n" + "=" * 70)
    print("5. DECRYPTION")
    print("=" * 70)

    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print("\nRecovered Plaintext:\n")

    for i in range(
        0,
        len(plaintext),
        80
    ):
        print(
            plaintext[
                i:i + 80
            ]
        )

    print("\n" + "=" * 70)
    print("6. VERIFICATION")
    print("=" * 70)

    verification = verify(
        plaintext,
        key,
        ciphertext
    )

    print(
        "\nRe-encryption matches "
        "original ciphertext:",
        "YES" if verification else "NO"
    )

    if verification:
        print(
            "Verification Successful."
        )
    else:
        print(
            "Verification Failed."
        )

    output_file = save_results(
        ciphertext,
        plaintext,
        key,
        estimated_key_length,
        verification
    )

    print(
        "\nResults saved to:",
        output_file
    )


if __name__ == "__main__":
    main()
