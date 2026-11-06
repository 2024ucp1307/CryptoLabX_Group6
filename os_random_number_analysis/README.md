
# Operating System Random Number Generation Analysis

## Objective
Evaluate operating-system random-number generation mechanisms
and investigate their suitability for cryptographic applications.

## Requirements
- Python 3
- NumPy
- SciPy
- Matplotlib
- Pandas
- OpenSSL
- Windows PowerShell and .NET (for Windows dataset)

## Installation

sudo apt install openssl
pip3 install numpy scipy matplotlib pandas

## Execution

python3 src/main.py

## Data Generation

1. Linux /dev/urandom
2. OpenSSL rand
3. Windows CNG/.NET RandomNumberGenerator

Run generate_windows.ps1 on Windows to generate the third dataset.

## Statistical Analysis

- Byte-frequency distribution
- Bit distribution
- Chi-square test
- Binomial test
- Repeated-pattern analysis
- Serial correlation
- Runs test

## Output

Statistical results:
outputs/results.txt

CSV results:
outputs/statistical_results.csv

Graphs:
outputs/graphs/

## Result

Random data was generated using operating-system
cryptographic random-number generation mechanisms.

Statistical tests were performed to investigate
the randomness properties of the generated data.

The results demonstrate that statistical randomness
alone cannot guarantee cryptographic security.
