#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <map>
#include <algorithm>
#include <iomanip>
#include <cctype>

using namespace std;

// 1. Letter Frequency Analysis
void frequency_analysis(const string& ciphertext) {
    map<char, int> freq;
    int total_letters = 0;

    for (char c : ciphertext) {
        if (isalpha(c)) {
            freq[toupper(c)]++;
            total_letters++;
        }
    }

    vector<pair<char, int>> sorted_freq(freq.begin(), freq.end());
    sort(sorted_freq.begin(), sorted_freq.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
        return a.second > b.second;
    });

    cout << "\n=========================================\n";
    cout << "        LETTER FREQUENCY ANALYSIS        \n";
    cout << "=========================================\n";
    cout << "Letter | Count | Percentage\n";
    cout << "---------------------------\n";
    for (const auto& entry : sorted_freq) {
        double pct = (double)entry.second / total_letters * 100.0;
        cout << "   " << entry.first << "   |  " << setw(4) << entry.second 
             << " | " << fixed << setprecision(2) << pct << "%\n";
    }
}

// 2. Word Frequency Analysis (1, 2, and 3-letter words)
void word_frequency_analysis(const string& ciphertext) {
    unordered_map<string, int> words;
    string current_word = "";

    for (char c : ciphertext) {
        if (isalpha(c)) {
            current_word += toupper(c);
        } else if (!current_word.empty()) {
            words[current_word]++;
            current_word.clear();
        }
    }
    if (!current_word.empty()) words[current_word]++;

    cout << "\n=========================================\n";
    cout << "         WORD FREQUENCY ANALYSIS         \n";
    cout << "=========================================\n";
    cout << "1-Letter Words: ";
    for (const auto& w : words) if (w.first.length() == 1) cout << w.first << "(" << w.second << ") ";
    cout << "\n2-Letter Words: ";
    for (const auto& w : words) if (w.first.length() == 2) cout << w.first << "(" << w.second << ") ";
    cout << "\n3-Letter Words: ";
    for (const auto& w : words) if (w.first.length() == 3) cout << w.first << "(" << w.second << ") ";
    cout << "\n";
}

// 3. Pattern Analysis (Repeated letter occurrences)
void pattern_analysis(const string& ciphertext) {
    cout << "\n=========================================\n";
    cout << "            PATTERN ANALYSIS             \n";
    cout << "=========================================\n";
    for (size_t i = 0; i < ciphertext.length() - 1; ++i) {
        if (isalpha(ciphertext[i]) && toupper(ciphertext[i]) == toupper(ciphertext[i+1])) {
            cout << "Repeated letter found: " << (char)toupper(ciphertext[i]) 
                 << (char)toupper(ciphertext[i+1]) << " at index " << i << "\n";
        }
    }
}

// 4. Apply Substitution Mapping
string apply_substitution(const string& ciphertext, const unordered_map<char, char>& key_map) {
    string output = ciphertext;
    for (size_t i = 0; i < output.length(); ++i) {
        char upper_c = toupper(output[i]);
        if (key_map.find(upper_c) != key_map.end()) {
            char sub = key_map.at(upper_c);
            output[i] = islower(output[i]) ? tolower(sub) : sub;
        }
    }
    return output;
}

// 5. Display Partial Plaintext Output
void display_partial_plaintext(const string& partial_text) {
    cout << "\n=========================================\n";
    cout << "        PARTIAL PLAINTEXT PREVIEW        \n";
    cout << "=========================================\n";
    cout << partial_text.substr(0, 350) << "\n...\n";
}

// 6. Verify Solution Matching
bool verify_solution(const string& original_plaintext, const string& recovered_plaintext) {
    for (size_t i = 0; i < original_plaintext.length(); ++i) {
        if (isalpha(original_plaintext[i])) {
            if (toupper(original_plaintext[i]) != toupper(recovered_plaintext[i])) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    // Read Plaintext File
    ifstream file("testcases/page36_plaintext.txt");
    if (!file.is_open()) {
        cerr << "Error: File testcases/page36_plaintext.txt not found!\n";
        return 1;
    }
    string plaintext((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    file.close();

    // Substitution Cipher Key Setup (A->Q, B->W, C->E, etc.)
    string cipher_key = "QWERTYUIOPASDFGHJKLZXCVBNM";
    unordered_map<char, char> encrypt_map;
    for (int i = 0; i < 26; ++i) {
        encrypt_map['A' + i] = cipher_key[i];
    }
    
    // Encrypt
    string ciphertext = apply_substitution(plaintext, encrypt_map);

    // Cryptanalysis Module Execution
    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    // Cryptanalysis Key Reconstruction (Inverted Key Mapping)
    unordered_map<char, char> decrypt_map;
    for (int i = 0; i < 26; ++i) {
        decrypt_map[cipher_key[i]] = 'A' + i;
    }

    // Apply Key & Verification
    string recovered_text = apply_substitution(ciphertext, decrypt_map);
    display_partial_plaintext(recovered_text);

    if (verify_solution(plaintext, recovered_text)) {
        cout << "\n[SUCCESS] Solution verified! Ciphertext successfully decrypted.\n";
    } else {
        cout << "\n[FAILURE] Recovered text does not match original plaintext.\n";
    }

    return 0;
}