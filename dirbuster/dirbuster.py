import requests
import argparse
import time 

from tqdm import tqdm
from colorama import Fore, Style
from urllib.parse import urlparse

def main():
    start_time = time.time() 

    print(r'''
    _____  _      ____              _            
    |  __ \(_)    |  _ \          | |           
    | |  | |_ _ __| |_) |_   _ ___| |_ ___ ____ 
    | |  | | | '__|  _ <| | | / __| __/ _ \  __|
    | |__| | | |  | |_) | |_| \__ \ ||  __/ |   
    |_____/|_|_|  |____/ \__,_|___/\__\___|_|  
    ''' + '\n')

    def enum(url): 
        if not urlparse(url).scheme:
            return 'http://' + url
        return url
    
    def get_response(url, timeout):
        try:
            response = requests.get(url, timeout=timeout) 

            if response.status_code >= 400:
                if response.status_code != 404: 
                    tqdm.write(Fore.YELLOW + f'[?] {url} {response.status_code}' + Style.RESET_ALL)
            elif response.status_code >= 500:
                tqdm.write(Fore.RED + f'[X] Something is wrong with the server')
                exit()
            else:
                tqdm.write(Fore.GREEN + f'[+] {url} {response.status_code}' + Style.RESET_ALL)

        # Checking for errors 
        except requests.ConnectionError:
            tqdm.write(Fore.RED + f'[X] Failed connection with {url}' + Style.RESET_ALL)
            exit()
        except requests.exceptions.Timeout:
            tqdm.write(Fore.YELLOW + f'[-] Timeout with {url}' + Style.RESET_ALL)
        except requests.RequestException as e:
            tqdm.write(Fore.RED + f'[X] Error with {url} : {e}' + Style.RESET_ALL)
        except KeyboardInterrupt:
            exit()

    def brute(base_url, timeout, extensions, wordlist): 
        base_url = enum(base_url).rstrip('/') 

        for word in tqdm(wordlist, desc="Scanning..."):
            word = word.strip()
            url = f"{base_url}/{word}"

            if extensions:
                for e in extensions:
                    get_response(url + '.' + e, timeout)
            get_response(url, timeout)
    
    parser = argparse.ArgumentParser()

    
    parser.add_argument('-u', '--url', help='set url for directory brute forcing', required=True)
    parser.add_argument(
    '-x', '--extensions',
    required=False,
    default=[],
    help='add custom extensions to check while brute forcing directories'
)

    parser.add_argument(
        '-t', '--timeout',            
        required=False,            
        type=int,
        default=3,
        help='set custom timeout for requests'            
)
    
    parser.add_argument(
        '-w', '--wordlist',
        required=True,            
        help='set wordlist to try directories from'            
)
    
    args = parser.parse_args()
    base_url = args.url
    wordlist = args.wordlist
    try:
        with open(wordlist, 'r') as f:
            wordlist = f.readlines()
    except FileNotFoundError:
        print(Fore.RED + f'[X] No such file or directory - {wordlist}' + Style.RESET_ALL)
        exit()

    timeout = args.timeout
    extensions = args.extensions
    extensions = extensions.split(',') if extensions else ''

    brute(base_url, timeout, extensions, wordlist) 

    print(f'\n[i] Time taken : {round(time.time() - start_time, 2)}s\n') 

if __name__ == '__main__':
    print('\n[!] Please, run the dirbuster.py in previous directory')