
# Miller-Rabin Prime Generation

## Objective
Generate a cryptographically secure probable prime
of exactly 512 bits using the Miller-Rabin primality test.

## Requirements
- Python 3
- SymPy

## Installation
pip install sympy

## Execution
python3 src/main.py

## Implementation
1. Generate random 512-bit odd candidates.
2. Apply Miller-Rabin primality testing.
3. Use 20 random bases for each candidate.
4. Repeat until a probable prime is found.
5. Verify the bit length.
6. Independently verify primality using SymPy.

## Output
Experimental results are automatically saved in:
outputs/results.txt

## Result
A 512-bit probable prime is successfully generated
and independently verified.
