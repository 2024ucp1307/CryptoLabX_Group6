# Vigenere Cipher Cryptanalysis Using Kasiski Examination and Frequency Analysis

## Assignment

Cryptanalysis of Vigenere Cipher using Kasiski Examination and Frequency Analysis.

**Group Number:** 6
**Ciphertext Used:** Ciphertext-2 (Even Group Numbers)

---

## Objective

The objective of this assignment is to recover the key and plaintext of a Vigenere-encrypted ciphertext without being given the key.

The cryptanalysis is performed using:

1. Kasiski Examination
2. Repeated pattern analysis
3. Distance calculation
4. Factor analysis
5. Index of Coincidence
6. Frequency analysis
7. Caesar shift estimation
8. Vigenere decryption
9. Re-encryption verification

---

## Directory Structure

```text
vigenere_cipher_attack/
├── README.md
├── src/
│   └── main.py
├── testcases/
│   └── ciphertext.txt
└── outputs/
    └── results.txt
```

---

## Input

The program uses the ciphertext assigned to Group 6.

Since Group 6 is an even-numbered group, **Ciphertext-2** is used.

The ciphertext is stored in:

```text
testcases/ciphertext.txt
```

The program automatically reads this file and does not require the user to enter a group number.

---

## Required Functions

The program implements the following user-defined functions:

```text
clean_ciphertext()
find_repeated_patterns()
calculate_distances()
find_factors()
kasiski_analysis()
calculate_ic()
split_into_groups()
frequency_analysis()
find_shift()
find_key()
vigenere_decrypt()
vigenere_encrypt()
verify()
```

---

## Algorithm

### 1. Preprocess the Ciphertext

The ciphertext is read from the input file.

Spaces, newlines and special characters are removed and all letters are converted to uppercase.

---

### 2. Find Repeated Patterns

Repeated sequences of length 3, 4 and 5 are searched for in the ciphertext.

The positions of repeated patterns are stored.

Repeated patterns are useful because their distances often contain multiples of the Vigenere key length.

---

### 3. Calculate Distances

For every repeated pattern, the distance between consecutive and multiple occurrences is calculated.

For example:

```text
Pattern: ABC
Positions: 10, 34, 58

Distances:
34 - 10 = 24
58 - 10 = 48
58 - 34 = 24
```

---

### 4. Find Factors

Factors of each distance are calculated.

Candidate key lengths from 2 to 20 are considered.

The frequency of each factor is counted. Factors occurring more frequently are stronger candidates for the key length.

---

### 5. Kasiski Analysis

The factor frequencies obtained from repeated-pattern distances are used to generate candidate key lengths.

The candidate lengths are then combined with Index of Coincidence analysis to select the most probable key length.

---

### 6. Calculate Index of Coincidence

For a text containing `N` letters, the Index of Coincidence is calculated as:

```text
IC = Σ fi(fi - 1) / N(N - 1)
```

where `fi` is the frequency of the `i`-th letter.

The ciphertext is divided according to different candidate key lengths and the average IC is calculated.

The key length giving the strongest IC evidence is selected.

---

### 7. Split the Ciphertext

Once the probable key length is obtained, the ciphertext is divided into groups.

For example, for a key length of 4:

```text
Group 1: positions 0, 4, 8, 12, ...
Group 2: positions 1, 5, 9, 13, ...
Group 3: positions 2, 6, 10, 14, ...
Group 4: positions 3, 7, 11, 15, ...
```

Each group behaves approximately like a Caesar cipher encrypted with one key character.

---

### 8. Frequency Analysis

Frequency analysis is performed separately for every group.

The program calculates the frequency of every letter from A to Z.

The observed frequencies are compared with standard English letter frequencies.

---

### 9. Determine Caesar Shift

For every group, all 26 possible Caesar shifts are tested.

Chi-square analysis is used to compare the shifted frequency distribution with English letter frequencies.

The shift having the smallest chi-square value is selected.

---

### 10. Recover the Key

The shifts obtained from all groups are converted into letters.

The letters are combined to form the probable Vigenere key.

For Group 6, the recovered key is:

```text
UNITEDSTATES
```

The estimated key length is:

```text
12
```

---

### 11. Decrypt the Ciphertext

The ciphertext is decrypted using the recovered key.

The standard Vigenere decryption formula is:

```text
P = (C - K) mod 26
```

where:

* `C` = ciphertext letter value
* `K` = key letter value
* `P` = plaintext letter value

---

### 12. Verify the Recovered Key

The recovered plaintext is encrypted again using the recovered key.

The regenerated ciphertext is compared with the original ciphertext.

The solution is considered verified only when:

```text
regenerated ciphertext == original ciphertext
```

---

## Results

For Group 6:

```text
Ciphertext: Ciphertext-2

Estimated Key Length: 12

Recovered Key: UNITEDSTATES
```

The recovered plaintext corresponds to a passage from the **United States Declaration of Independence**.

The plaintext is displayed without spaces and punctuation because the ciphertext preprocessing removes non-alphabetic characters.

---

## Verification

The recovered plaintext is re-encrypted using the recovered key.

The regenerated ciphertext is compared character-by-character with the original ciphertext.

Expected result:

```text
Re-encryption matches original ciphertext: YES
Verification Successful.
```

---

## How to Run

From the repository root:

```bash
python3 attacks/vigenere_cipher_attack/src/main.py
```

The program directly uses the Group 6 ciphertext stored in:

```text
attacks/vigenere_cipher_attack/testcases/ciphertext.txt
```

No group number or additional input is required.

---

## Output

The program displays:

* repeated patterns
* positions of repeated patterns
* distances between repeated patterns
* Kasiski candidate key lengths
* estimated key length
* Index of Coincidence
* ciphertext groups
* A-Z frequency tables for every group
* probable Caesar shift for every group
* recovered Vigenere key
* recovered plaintext
* re-encryption verification

The final results are also saved in:

```text
attacks/vigenere_cipher_attack/outputs/results.txt
```

---

## Conclusion

The Vigenere ciphertext assigned to Group 6 was successfully cryptanalysed using Kasiski Examination and frequency analysis.

The probable key length was determined as 12 and the recovered key was:

```text
UNITEDSTATES
```

The recovered plaintext produced meaningful English text, and re-encryption using the recovered key reproduced the original ciphertext, confirming the correctness of the recovered solution.
