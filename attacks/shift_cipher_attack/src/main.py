import os
import json
from shift_cipher import ShiftCipher
from brute_force_dictionary import DictionaryAttack
from chi_square_attack import ChiSquareAttack

def run():
    dict_path = os.path.join("dictionary", "english_words.txt")
    dict_solver = DictionaryAttack(dict_path)
    chi_solver = ChiSquareAttack()
    
    test_cases = [
        {"id": "TC1", "text": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", "actual_key": 7},
        {"id": "TC2", "text": "ATTACK AT DAWN", "actual_key": 13},
        {"id": "TC3", "text": "CRYPTOGRAPHY AND NETWORK SECURITY", "actual_key": 3},
        {"id": "TC4", "text": "KUBERNETES POD", "actual_key": 18} # Demonstrates OOV failure
    ]

    # Export Testcases
    os.makedirs("testcases", exist_ok=True)
    with open("testcases/cases.json", "w") as f:
        json.dump(test_cases, f, indent=4)

    os.makedirs("outputs", exist_ok=True)
    
    table_header = f"{'Test Case':<10} | {'Actual Key':<10} | {'Dict Key':<10} | {'Chi Key':<10} | {'Dict Correct?':<13} | {'Chi Correct?'}"
    divider = "-" * 80
    
    print(table_header)
    print(divider)
    
    output_lines = [table_header, divider]

    for tc in test_cases:
        ciphertext = ShiftCipher.encrypt(tc["text"], tc["actual_key"])
        
        dict_key = dict_solver.solve(ciphertext)
        chi_key = chi_solver.solve(ciphertext)
        
        dict_corr = "Yes" if dict_key == tc["actual_key"] else "No"
        chi_corr = "Yes" if chi_key == tc["actual_key"] else "No"
        
        row = f"{tc['id']:<10} | {tc['actual_key']:<10} | {dict_key:<10} | {chi_key:<10} | {dict_corr:<13} | {chi_corr}"
        print(row)
        output_lines.append(row)

    with open("outputs/results.txt", "w") as f:
        f.write("\n".join(output_lines))

if __name__ == "__main__":
    run()