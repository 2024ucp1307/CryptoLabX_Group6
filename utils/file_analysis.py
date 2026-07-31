import os
from collections import Counter

def analyze_file(filename):
    filepath = os.path.join("datasets", filename)

    if not os.path.exists(filepath):
        print("\nError: File not found!")
        return

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Number of characters
    characters = len(content)

    # Number of words
    words = len(content.split())

    # Number of lines
    lines = content.count("\n") + 1 if content else 0

    # Number of unique characters
    unique_characters = len(set(content))

    # Letter frequency (only alphabets)
    letters = [ch.lower() for ch in content if ch.isalpha()]
    frequency = Counter(letters)

    print("\n========== File Analysis ==========")
    print(f"Characters        : {characters}")
    print(f"Words             : {words}")
    print(f"Lines             : {lines}")
    print(f"Unique Characters : {unique_characters}")

    print("\nLetter Frequency")
    print("----------------")

    for letter in sorted(frequency):
        print(f"{letter} : {frequency[letter]}")
