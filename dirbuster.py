import requests, argparse, sys, time
from tqdm import tqdm
from colorama import Fore, Style
from urllib.parse import urlparse

# Options:
#
# --extensions : Set the extensions to test (none by default)
# --timeout : Set timeout in seconds (1 second by default)
#
# Usage examples:
#
# cat wordlist.txt (or your wordlist) | python dirbuster.py https://example.com
# Standard directory brute force with no tweaks
#
# cat wordlist.txt | python dirbuster.py https://example.com --timeout 5
# If the site doesn't respond or can't connect, will wait 5 seconds before trying new one
#
# cat wordlist.txt | python dirbuster.py https://example.com --extensions php html txt 
# Will check the directories from wordlist with provided extensions
#
# cat wordlist.txt | python dirbuster.py https://example.com --timeout 3 --extensions php html text
# Combination of two last examples, will not only check the directories with provided extensions,
# but also disconnect and try a new directory if a site doesn't respond for 3 seconds
#
# Tip: Do not add too many extensions, will take a veeeeeery looooong time

def main():
    start_time = time.time() 
    count = 0

    print(r'''
    _____  _      ____              _            
    |  __ \(_)    |  _ \          | |           
    | |  | |_ _ __| |_) |_   _ ___| |_ ___ _ __ 
    | |  | | | '__|  _ <| | | / __| __/ _ \ '__|
    | |__| | | |  | |_) | |_| \__ \ ||  __/ |   
    |_____/|_|_|  |____/ \__,_|___/\__\___|_|  
    ''' + '\n')

    def enum(url): # Checking the url for a scheme (http:// or https://)
        if not urlparse(url).scheme:
            return 'http://' + url
        return url

    def brute(base_url, timeout, extensions, wordlist): # Main function for bruteforcing directories
        nonlocal count
        base_url = enum(base_url).rstrip('/') # Preparing the url

        for word in tqdm(wordlist, desc="Scanning..."):
            word = word.strip()
            urls = [f"{base_url}/{word}"] # Adding the base url to the list of urls for checking

            if extensions:
                for e in extensions:
                    urls.append(f"{base_url.rstrip('/')}/{word}.{e}") # Add extensions and check them if they have been provided
                
            for url in urls:
                try:
                    response = requests.get(url, timeout=timeout) # Trying to connect to the site

                    if response.status_code < 400: # Checking the status code
                        count += 1
                        tqdm.write(Fore.GREEN + f'[+] Found {url} {response.status_code}' + Style.RESET_ALL) 

                # Checking for errors 
                except requests.ConnectionError:
                    tqdm.write(Fore.RED + f'[X] Failed connection with {url}' + Style.RESET_ALL)
                except requests.exceptions.Timeout:
                    tqdm.write(Fore.YELLOW + f'[-] Timeout with {url}' + Style.RESET_ALL)
                except requests.RequestException as e:
                    tqdm.write(Fore.RED + f'[X] Error with {url} : {e}' + Style.RESET_ALL)

    # Parser
    parser = argparse.ArgumentParser()

    # Adding arguments
    parser.add_argument('base_url')
    parser.add_argument(
    '--extensions',
    nargs='+',
    default=[],
)

    parser.add_argument(
        '--timeout',
        nargs='?',            
        const=1,              
        type=int,
        default=1,            
)
    
    args = parser.parse_args() # Parse arguments
    wordlist = [line for line in sys.stdin] # Preparing the wordlist


    brute(args.base_url, args.timeout, args.extensions, wordlist) # Start the bruteforce

    print(f'\n[i] Directories found : {count}')  # Write out stats
    print(f'[i] Time taken : {round(time.time() - start_time, 2)}\n')

if __name__ == '__main__':
    main() # Running the script
