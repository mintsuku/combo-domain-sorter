import os
os.environ['PYTHONWARNINGS'] = 'ignore::Warning'

import re
import threading
import time
from collections import defaultdict
from tkinter import filedialog, Tk
from colored import fg

green = fg(2)
reset = fg(7)
red = fg(1)

def logo():
    print(rf"""{red}
                    
    
                      _____                        _          _____            _            
                     |  __ \                      (_)        / ____|          | |           
                     | |  | | ___  _ __ ___   __ _ _ _ __   | (___   ___  _ __| |_ ___ _ __ 
                     | |  | |/ _ \| '_ ` _ \ / _` | | '_ \   \___ \ / _ \| '__| __/ _ \ '__|
                     | |__| | (_) | | | | | | (_| | | | | |  ____) | (_) | |  | ||  __/ |   
                     |_____/ \___/|_| |_| |_|\__,_|_|_| |_| |_____/ \___/|_|   \__\___|_|   

                                                Mox <3 @millymox                                                                   
                                                                        

    
    {reset}""")

def extract_domain(email):
    domain = re.search("@[\w.]+", email)
    return domain.group() if domain else None

def write_combos(domain, combo_list):
    output_file = f"output/{domain[1:]}_combos.txt"
    with open(output_file, "w") as outfile:
        for email, password in combo_list:
            outfile.write(f"{email}:{password}\n")

def process_file(input_file):
    combos = defaultdict(list)
    start_time = time.time()
    with open(input_file, "r") as infile:
        for line in infile:
            email, password = line.strip().split(":", 1)
            domain = extract_domain(email)
            if domain:
                combos[domain].append((email, password))
                print(f"{green}[+] - {email}:{password}{reset}")

    os.makedirs("output", exist_ok=True)

    threads = []
    for domain, combo_list in combos.items():
        if domain:
            thread = threading.Thread(target=write_combos, args=(domain, combo_list))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    processing_time = round(time.time() - start_time, 2)
    num_domains = len(combos)
    print("                     ")
    print("                     ")
    print(f"Sorted {green}{num_domains}{reset} domains in {green}{processing_time}{reset} seconds")

def main():
    logo()
    input(f"{green}[+] Insert Combos {reset}")
    
    root = Tk()
    root.withdraw()  # Hide the empty tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], parent=root)
    root.destroy()
    
    if file_path:
        process_file(file_path)

if __name__ == "__main__":
    main()
