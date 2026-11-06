
import os
import subprocess
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.stats import chisquare, binomtest, norm

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
GRAPH_DIR = OUTPUT_DIR / "graphs"

SIZE = 1024 * 1024  # 1 MB (1 MiB)

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
GRAPH_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
# PART 1: RANDOM DATA GENERATION
# -------------------------------------------------

def generate_urandom():
    print("\nGenerating data using /dev/urandom...")

    path = DATA_DIR / "urandom.bin"
    start = time.perf_counter()

    with open("/dev/urandom", "rb") as source:
        data = source.read(SIZE)

    path.write_bytes(data)

    print("Generated:", len(data), "bytes")
    print("Time:", round(time.perf_counter() - start, 4), "seconds")


def generate_openssl():
    print("\nGenerating data using OpenSSL rand...")

    path = DATA_DIR / "openssl_rand.bin"
    start = time.perf_counter()

    subprocess.run(
        ["openssl", "rand", "-out", str(path), str(SIZE)],
        check=True
    )

    print("Generated:", path.stat().st_size, "bytes")
    print("Time:", round(time.perf_counter() - start, 4), "seconds")


# -------------------------------------------------
# PART 2: STATISTICAL ANALYSIS
# -------------------------------------------------

def analyze_random_data(name, data):

    print("\nAnalyzing:", name)

    n = len(data)

    # Byte frequency distribution
    frequency = np.bincount(data, minlength=256)

    expected = np.full(256, n / 256)

    chi_stat, chi_p = chisquare(
        frequency,
        f_exp=expected
    )

    # Bit distribution
    bits = np.unpackbits(data)

    ones = int(np.sum(bits))
    zeros = len(bits) - ones

    bit_percentage = (ones / len(bits)) * 100

    bit_p = binomtest(
        ones,
        len(bits),
        0.5
    ).pvalue

    # Repeated adjacent bytes
    repeated_bytes = int(
        np.sum(data[1:] == data[:-1])
    )

    repeated_rate = repeated_bytes / (n - 1)

    # Repeated non-overlapping 16-byte blocks
    blocks = data[:(n // 16) * 16].reshape(-1, 16)

    unique_blocks = np.unique(
        blocks,
        axis=0
    ).shape[0]

    repeated_blocks = len(blocks) - unique_blocks

    # Serial correlation (lag 1)
    x = data[:-1].astype(np.float64)
    y = data[1:].astype(np.float64)

    serial_corr = np.corrcoef(x, y)[0, 1]

    # Runs test on individual bits
    bit_runs = np.count_nonzero(bits[1:] != bits[:-1]) + 1

    pi = ones / len(bits)
    bit_count = len(bits)

    if abs(pi - 0.5) < 2 / np.sqrt(bit_count):
        expected_runs = 2 * bit_count * pi * (1 - pi)

        run_std = 2 * np.sqrt(2 * bit_count) * pi * (1 - pi)

        run_z = (bit_runs - expected_runs) / run_std

        runs_p = 2 * norm.sf(abs(run_z))
    else:
        run_z = float("nan")
        runs_p = float("nan")

    # Display results
    print("\nBYTE FREQUENCY")
    print("Chi-square statistic:", chi_stat)
    print("Chi-square p-value:", chi_p)

    print("\nBIT DISTRIBUTION")
    print("Zero bits:", zeros)
    print("One bits:", ones)
    print("Percentage of ones:", bit_percentage)
    print("Binomial test p-value:", bit_p)

    print("\nREPEATED PATTERNS")
    print("Adjacent repeated bytes:", repeated_bytes)
    print("Adjacent repeat rate:", repeated_rate)
    print("Duplicate 16-byte blocks:", repeated_blocks)

    print("\nSERIAL CORRELATION")
    print("Lag-1 correlation:", serial_corr)

    print("\nRUNS TEST")
    print("Number of runs:", bit_runs)
    print("Z statistic:", run_z)
    print("Runs test p-value:", runs_p)

    # Byte frequency graph
    plt.figure(figsize=(12, 4))

    plt.bar(range(256), frequency)

    plt.axhline(
        n / 256,
        color="red",
        linestyle="--",
        label="Expected frequency"
    )

    plt.title(f"Byte Frequency - {name}")
    plt.xlabel("Byte Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

    plt.savefig(GRAPH_DIR / f"{name}_frequency.png")
    plt.close()

    # Bit distribution graph
    plt.figure(figsize=(5, 4))

    plt.bar(
        ["Zero", "One"],
        [zeros, ones]
    )

    plt.title(f"Bit Distribution - {name}")
    plt.ylabel("Number of Bits")
    plt.tight_layout()

    plt.savefig(GRAPH_DIR / f"{name}_bits.png")
    plt.close()

    return {
        "Source": name,
        "Bytes": n,
        "Chi-square": chi_stat,
        "Byte p-value": chi_p,
        "Zero bits": zeros,
        "One bits": ones,
        "One percentage": bit_percentage,
        "Bit p-value": bit_p,
        "Adjacent repeats": repeated_bytes,
        "Repeated 16-byte blocks": repeated_blocks,
        "Serial correlation": serial_corr,
        "Runs": bit_runs,
        "Runs Z": run_z,
        "Runs p-value": runs_p
    }


# -------------------------------------------------
# PART 3: LOAD DATASETS AND COMPARE
# -------------------------------------------------

def main():

    print("=" * 60)
    print("OPERATING SYSTEM RANDOM NUMBER ANALYSIS")
    print("=" * 60)

    # Generate Linux datasets
    if os.name == "posix":
        generate_urandom()
        generate_openssl()
    else:
        print("Linux generation skipped on this operating system.")

    datasets = {
        "Linux urandom": DATA_DIR / "urandom.bin",
        "OpenSSL rand": DATA_DIR / "openssl_rand.bin",
        "Windows CNG": DATA_DIR / "windows_cng.bin"
    }

    results = []

    for name, path in datasets.items():

        if not path.exists():
            print("\nDataset missing:", name)
            continue

        data = np.fromfile(
            path,
            dtype=np.uint8
        )

        if len(data) < SIZE:
            print("Insufficient data:", name)
            continue

        # Use equal-sized samples
        data = data[:SIZE]

        result = analyze_random_data(name, data)

        results.append(result)

    if not results:
        print("No datasets available for analysis.")
        return

    # Save results as CSV
    df = pd.DataFrame(results)

    csv_path = OUTPUT_DIR / "statistical_results.csv"
    df.to_csv(csv_path, index=False)

    # Save results as text
    text_path = OUTPUT_DIR / "results.txt"

    with open(text_path, "w") as file:
        file.write("OPERATING SYSTEM RANDOM NUMBER ANALYSIS\n")
        file.write("=" * 60 + "\n\n")
        file.write(df.to_string(index=False))
        file.write("\n\nSTATISTICAL INTERPRETATION\n")
        file.write(
            "A p-value >= 0.05 means the test did not detect "
            "a significant deviation at the 5% level.\n"
        )
        file.write(
            "It does not prove cryptographic security.\n"
        )

    print("\n" + "=" * 60)
    print("COMPARISON TABLE")
    print("=" * 60)

    print(df.to_string(index=False))

    print("\nResults saved to:", text_path)
    print("CSV saved to:", csv_path)
    print("Graphs saved to:", GRAPH_DIR)


if __name__ == "__main__":
    main()
