from datetime import datetime
import os

def write_log(choice):
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/logfile.txt", "a") as file:
        file.write(f"{datetime.now()} : Selected Option {choice}\n")
