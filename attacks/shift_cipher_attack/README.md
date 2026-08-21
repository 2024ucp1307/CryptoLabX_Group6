# Cryptanalysis of Shift Cipher

This module implements cryptanalysis techniques against the Shift Cipher: Brute-Force Dictionary Scoring and Chi-Square Distribution Analysis[cite: 1].

## Section 1: Cryptanalysis Algorithms
* **Dictionary Scoring:** Evaluates all 26 decryption shifts. Tokenizes each decrypted text and counts matches against `english_words.txt`. The key with the highest count wins.
* **Chi-Square Analysis:** Computes observed character frequencies for each candidate shift and compares them to standard English letter probabilities via the $\chi^2$ goodness-of-fit statistic:
  $$\chi^2 = \sum_{i=A}^{Z} \frac{(O_i - E_i)^2}{E_i}$$

## Section 2: Comparison
| Metric | Dictionary Scoring | Chi-Square Analysis |
| :--- | :--- | :--- |
| **Ideal Text Length** | Effective on short texts with clear spaces | Requires longer text (>100 characters) |
| **Vocabulary Dependency** | Fails on Out-of-Vocabulary (OOV) words | Vocabulary-independent |
| **Complexity** | $O(26 \times W)$ where $W$ = word count | $O(26 \times N)$ where $N$ = char count |

## Section 3: Failure Analysis
* **Dictionary Attack:** Fails when plaintext contains proper nouns, jargon, or unspaced text. *Improvement:* Use character $n$-gram probability scoring.
* **Chi-Square Attack:** Fails on short ciphertexts or lipograms due to statistical variance from standard English frequencies. *Improvement:* Combine with Index of Coincidence (IC) thresholds.

## Section 4: Observations & Conclusion
* Chi-Square scales reliably for standard long texts without needing a large dictionary.
* Both methods process small key spaces ($K=26$) in sub-millisecond execution times.