import requests
import json
import os
from datetime import datetime
from colorama import Fore, Style
from halo import Halo
os.system('clear')
def validate_dob_format(dob):
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_nid_format(nid):
    return len(nid) in [10, 13, 17]

def main():
    ascii_art = r'''  _   _ ___ ____  _  _____ _____
 | \ | |_ _|  _ \| |/ /_ _|_   _|
 |  \| || || | | | ' / | |  | |
 | |\  || || |_| | . \ | |  | |
 |_| \_|___|____/|_|\_\___| |_|'''

    developer_info = ''' [+] DEVELOPER : XYRUS INC
 [+] TELEGRAM  : @XYRUSINC'''

    print(Fore.RED + ascii_art + Style.RESET_ALL)
    print(developer_info)

    config_file_path = 'config.json'
    if not os.path.isfile(config_file_path):
        print(Fore.RED + "Error: config.json file not found." + Style.RESET_ALL)
        return

    try:
        with open(config_file_path) as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get('key')

            if not api_key:
                print(Fore.RED + "Error: 'key' not found in config.json." + Style.RESET_ALL)
                return

            headers = {
                'Content-Type': 'application/json',
            }

            nid = input(Fore.GREEN + " [+] Enter NID : " + Style.RESET_ALL)
            dob = input(Fore.GREEN + " [+] Enter DOB (YYYY-MM-DD) : " + Style.RESET_ALL)

            if not validate_nid_format(nid):
                print(Fore.RED + " [-] Error: Invalid NID format." + Style.RESET_ALL)
                return

            if not validate_dob_format(dob):
                print(Fore.RED + " [-] Error: Invalid DOB format." + Style.RESET_ALL)
                return

            json_data = {
                'key': api_key,
                'nid': nid,
                'dob': dob,
            }
            spinner = Halo(text='[+] Please wait Searching Nid information...', spinner='dots12')
            
            spinner.start()

            response = requests.post('https://textly.one/api/v1/nid', headers=headers, json=json_data)
            spinner.stop()
            os.system("clear")
            if response.status_code == 200:
                data = response.json()
                for key, value in data.items():
                    print(Fore.YELLOW + "❏ " + key.upper() + ":" + Style.RESET_ALL, end=" ")
                    if isinstance(value, dict):
                        print()
                        for nested_key, nested_value in value.items():
                            print("\t" + Fore.CYAN + "❏ " + nested_key.upper() + ":" + Style.RESET_ALL, nested_value)
                    else:
                        print(value)
            else:
                y = json.loads(response.text)
                error_message = y.get('msg')
                print(Fore.RED + "Error: Nid information not found!" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + " [-] Error: config.json file not found." + Style.RESET_ALL)
        return
    except json.JSONDecodeError:
        print(Fore.RED + " [-] Error: Invalid JSON response." + Style.RESET_ALL)
        return

if __name__ == "__main__":
    main()
